## Modeling Citation Trajectories of Scientific Papers
* This repository contains the code and data required to reproduce the results reported in the paper.
* The following sections contain instructions on running the models.

### Evaluation Model
* `javac CitationPattern.java`
* `java CitationPattern.class ACTIVATION_PERIOD PEAK_THRESHOLD` to classify the nodes, according to the specified parameters.

### Ground-truth network
* `python generate_gt_net.py`

### Barabasi-ALbert, Additive-fitness, Multiplicative-fitness models
* `python main_<ba,add,mult>.py --out_suffix OUT_SUFFIX --track_till GROW_TILL --num_threads 0`
* The argument `GROW_TILL` should have the year till which we want to grow the network. This means, only the nodes published till the year `GROW_TILL - 10` will be classified by the evaluation model.

### LBM
* `python main_lbm.py --out_suffix OUT_SUFFIX --track_till GROW_TILL --num_threads 0 --gamma GAMMA`
* The argument `GROW_TILL` should have the year till which we want to grow the network. This means, only the nodes published till the year `GROW_TILL - 10` will be classified by the evaluation model.
* The argument `GAMMA` represents the type of function mapped from the number of nodes in the network. The options are `constant`, `linear`, `sqrt` and `log`.

### LBM
* `python main_lbm.py --out_suffix OUT_SUFFIX --track_till GROW_TILL --num_threads 0 --skip SKIP --stdev STDEV`
* The argument `GROW_TILL` should have the year till which we want to grow the network. This means, only the nodes published till the year `GROW_TILL - 10` will be classified by the evaluation model.
* The argument `SKIP` represents the frequency at which the active subspace is shifted. A negative value means the frequency is in terms of months, while a positive value means the frequency is in terms of number of new nodes entering the network.
* The argument `STDEV` represents the standard deviation of the Gaussian distribution over each active subspace, from which location vectors are sampled and assigned to nodes.