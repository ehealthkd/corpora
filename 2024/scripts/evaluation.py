"""
Usage: python evaluation.py --pathDataInfered <path to estimations> --pathDataGold <path to gold>
"""

#Importing the required libraries
import argparse
import pandas as pd
import json

#Parse the arguments
# - Data infered path: pathDataInfered
# - Data real path: pathDataGold

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--pathDataInfered', metavar='pathDataInfered', type=str, help='Path to the data infered')
parser.add_argument('--pathDataGold', metavar='pathDataGold', type=str, help='Path to the data real')


pathDataInfered = parser.parse_args().pathDataInfered
pathDataGold = parser.parse_args().pathDataGold


dataInfered = pd.read_csv(pathDataInfered, sep=",")
dataGold = pd.read_csv(pathDataGold, sep=",")


catList = ['AminoAcidPeptideOrProtein', 'AnatomicalAbnormality', 'Bacterium', 'BiologicFunction', 'BiologicallyActiveSubstance', 'BiomedicalOccupationOrDiscipline', 'BodyPartOrganOrOrganComponent', 'Cell', 'CellComponent', 'CellFunction', 'CellOrMolecularDysfunction', 'Chemical', 'ClinicalAttribute', 'DiseaseOrSyndrome', 'EmbryonicStructure', 'EnvironmentalEffectOfHumans', 'Eukaryote', 'ExperimentalModelOfDisease', 'Finding', 'GeneOrGenome', 'HealthCareActivity', 'HealthCareRelatedOrganization', 'IndividualBehavior', 'InjuryOrPoisoning', 'MachineActivity', 'ManufacturedObject', 'MolecularSequence', 'NaturalPhenomenonOrProcess', 'NucleicAcidNucleosideOrNucleotide', 'Organism', 'OrganismAttribute', 'PathologicFunction', 'PatientOrDisabledGroup', 'PharmacologicSubstance', 'PopulationGroup', 'ResearchActivity', 'SignOrSymptom', 'Substance', 'TemporalConcept', 'Virus']


#CLASIFICACIÓN DE ELEMENTOS
def detectAndClassifyTexts(textTag, df):

    #Order the real and predicted arrays by start, and if start is the same, by tag
    real      = sorted(textTag['real'],      key = lambda row: (row["start"], row["tag"]))
    predicted = sorted(textTag['predicted'], key = lambda row: (row["start"], row["tag"]))

    #CORRECT - Ca
    for annR in real.copy():
        for annP in predicted.copy():
            if annR['start'] == annP['start'] and annR['end'] == annP['end'] and annR['tag'] == annP['tag']:
                
                df.loc[annR['tag'], 'Ca'] += 1

                real.remove(annR)
                predicted.remove(annP)

                break

    #PARTIAL - Ca
    for annR in real.copy():
        #Get all the annotation within the range of the real annotation
        partialMatch = []
        
        for annP in predicted.copy():
            if (annP['start'] >= annR['start'] and annP['end'] <= annR['end']) or \
            (annP['start'] <= annR['start'] and annP['end'] >= annR['start'] and annP['end'] <= annR['end']) or \
            (annP['start'] >= annR['start'] and annP['start'] <= annR['end'] and annP['end'] >= annR['end']) or \
            (annP['start'] <= annR['start'] and annP['end'] >= annR['end']):
                
                #Append the element to the partialMatch array
                partialMatch.append(annP)

        if len(partialMatch) != 0:
                
                #Order the partialMatch elements by size (end - start)
                partialMatch = sorted(partialMatch, key = lambda row: (row["end"] - row["start"]))

                #Check if some of the element tags are the same as the real annotation
                for annP in partialMatch:
                    if annP['tag'] == annR['tag']:
                        df.loc[annR['tag'], 'Pa'] += 1
                        real.remove(annR)
                        predicted.remove(annP)
                        break
                    
    #INCORRECT - Ia
    for annR in real.copy():
        for annP in predicted.copy():
            if annP['start'] == annR['start'] and annP['end'] == annR['end'] and annP['tag'] != annR['tag']:
                
                df.loc[annR['tag'], 'Ia'] += 1

                real.remove(annR)
                predicted.remove(annP)

                break

    #MISSING - Ma
    for annR in real.copy():
        df.loc[annR['tag'], 'Ma'] += 1


    #SPURIOUS - Sa
    for annP in predicted:
        df.loc[annP['tag'], 'Sa'] += 1

    del real, predicted
    
    return df


def evalDataset(real, predicted, catList):

    df = pd.DataFrame(columns=['Ca', 'Ia', 'Pa', 'Ma', 'Sa', 'Precision', 'Recall', 'F1', 'Accuracy'], index=catList)
    df = df.fillna(0)

    #Iterate over the real and predicted dataframes
    

    for indexI, rowI in predicted.iterrows():
        for indexR, rowR in real.iterrows():
            #Check if the id and the text are the same
            if rowI.ID == rowR.ID and rowI.TEXT == rowR.TEXT:
                textTag = {'real': json.loads(rowR.TAGS.replace("'", '"')), 'predicted': json.loads(rowI.TAGS.replace("'", '"'))}
                df = detectAndClassifyTexts(textTag, df)


    #Calculate precision, recall, F1 and accuracy
    df['Precision'] = (df['Ca'] + 0.5 * df['Pa']) / (df['Ca'] + df['Ia'] + df['Pa'] + df['Sa'])
    df['Recall'] = (df['Ca'] + 0.5 * df['Pa']) / (df['Ca'] + df['Ia'] + df['Pa'] + df['Ma'])
    df['F1'] = 2 * (df['Precision'] * df['Recall']) / (df['Precision'] + df['Recall'])
    df['Accuracy'] = (df['Ca'] + 0.5 * df['Pa']) / (df['Ca'] + df['Ia'] + df['Pa'] + df['Ma'] + df['Sa'])

    #Delete rows where Ca,Ia, Pa, Ma and Sa are all 0
    df = df[(df.T != 0).any()]

    #Fill the NaN values with 1
    df = df.fillna(1)

    for row in df.index:
        if df.loc[row, 'Ca'] == 0 and df.loc[row, 'Pa'] == 0 and df.loc[row, 'Ia'] == 0 and df.loc[row, 'Ma'] == 0 and df.loc[row, 'Sa'] == 0:
            df = df.drop(row)

    precision = (df['Ca'].sum() + 0.5 * df['Pa'].sum()) / (df['Ca'].sum() + df['Ia'].sum() + df['Pa'].sum() + df['Sa'].sum())
    recall = (df['Ca'].sum() + 0.5 * df['Pa'].sum()) / (df['Ca'].sum() + df['Ia'].sum() + df['Pa'].sum() + df['Ma'].sum())
    F1 = 2 * (precision * recall) / (precision + recall)
    accuracy = (df['Ca'].sum() + 0.5 * df['Pa'].sum()) / (df['Ca'].sum() + df['Ia'].sum() + df['Pa'].sum() + df['Ma'].sum() + df['Sa'].sum())

    #Get the average metrics of each dataframe
    infoMetrics = [{'Precision': precision, 'Recall': recall, 'F1': F1, 'Accuracy': accuracy}]
    
    return [df, infoMetrics]


df, metrics  = evalDataset(dataGold, dataInfered, catList)

#Print the metrics
print("Precision: ", metrics[0]['Precision'])
print("Recall: ", metrics[0]['Recall'])
print("F1: ", metrics[0]['F1'])
print("Accuracy: ", metrics[0]['Accuracy'])

#Save the df of the metrics
df.to_csv('metrics.csv', index=True)

#Save the metrics
with open('metrics.json', 'w') as outfile:
    json.dump(metrics, outfile)


