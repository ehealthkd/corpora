# Testing data

This folder contains the testing data in evaluation format, i.e., divided by scenarios. Now that the challenge is over, the corresponding `output.*` files are also provided for self-evaluation.

The folder `scenario1-main` contains `3000` sentences. The first `2700` are in Spanish and the last `300` are in English. Of these, only `50` in each language will be used for evaluation (the rest are provided to discourage manual annotation), but you must output annotations for all of the sentences, since the reference sentences are shuffled.

Teams that prefer to participate only in one language can ignore the remaining sentences and not output annotations for them. **However**, make sure to respect character positions to maintain the alignment with the reference annotations. For example, if you are ignoring the Spanish sentences, then your first entity annotation should start around char 195,700 which is roughly where English sentences begin.

Folders `scenario2-taskA` and `scenario3-taskB` contains `50` Spanish sentences and `50` English sentences in that order.

In respect of the ethics of the competition, we kindly ask participants **not** to manually review the testing output, beyond the minimum necessary to guarantee there are no implementation errors. Especially, please do not manually annotate any of the test-set sentences, evaluate your predicted annotations, or make any design decision based on perceived performance of the test set. Doing so would incur in overfitting the testing data and diminish the value of the challenge for all participants.
