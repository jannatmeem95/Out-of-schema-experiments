The "data" folder contains both of our created datasets (D-MultiWoz and D-SGD).

Pre-processing: The codes for transforming the dataset is in folder named "processing"

Commands: 

python3 insertQuestions.py
python3 insertDid.py

It transforms the original data stored in folder "input/dialogues" to our D-MultiWoz dataset and stores it in the "data" folder. 


Out-of-schema Question Detection: The codes for GPT Out-of-schema Question Detection are in the folder named ChatGPT.

Commands:
For Out-of-schema Question Detection, run ./run_gpt_detection.sh $datasetName $model-choice
For evaluation, run ./run_evaluation.sh $datasetName $model-choice

$datasetName choices are: MultiWoz, SGD, DSTC
$model-choice should "4" for GPT-4 and anything else for GPT-3.5


OQS Algorithm: The codes for OQS algorithm and simulation are in the folder named "newApproach".

Commands:
python3 1_get_convo_sequence.py
python3 2_MarkovRank.py $Pr_wd$ $Pr_sq$
python3 3_working_clustering.py
python3 4_BenefitCluster.py $Pr_wd$ $dataset$ (dataset is either "DSGD" or "DMultiWoz")
python3 5_simulation.py $Pr_wd$ $dataset$ 
python3 6_simulation_cluster.py $Pr_wd$ $dataset$ 


The ranked results are stored in folder: "newApproach/$dataset$/ranked_results"
The simulation results are stored in folder: "newApproach/$dataset$/simulation_output"
