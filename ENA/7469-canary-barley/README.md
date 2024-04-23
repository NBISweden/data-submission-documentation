---
Redmine_issue: https://projects.nbis.se/issues/7469
Repository: ENA
Submission_type: exome # e.g. metagenome, WGS, assembly, - IF RELEVANT
Data_generating_platforms:
- NGI
Top_level_acccession: PRJEB75210
---

# 7469 Canary barley

## Submission task description
Help with long-term archiving of raw sequence reads from 17 individuals. Data is NGS sequencing of exome capture from barley (Hordeum vulgare).

## Procedure overview and links to examples

* Collect metadata in [template](./data/7469-barley-metadata_template_default_ERC000011.xlsx)
* Transfer sequence files to ENA, using Aspera on interactive node
* Submit study
* Submit samples
* Submit experiments

## Lessons learned
* PI did not have a gmail so instead of sharing metadata template on google drive, we did it the old way by sending an excel file back and forth. While not ideal, it worked this time since the PI didn't need any assistance with filling the template.
* PI added me to ENA account upon creation of account, so I received an email with the username
* PI sent me the password via SMS, which seems as a safe enough way

## Detailed step by step description

### Collect metadata
* I created a metadata template using the default checklist (ERC000011) and shared with PI who filled it in without any major issues

### Data transfer
* Data transfer is done at Uppmax using Aspera:
```
interactive -t 08:00:00 -A naiss2024-22-345
module load ascp
export ASPERA_SCP_PASS='password'
./go-ascp.sh &
```
* I kept an eye on the ENA upload area using FileZilla

### Submit study
* Study submission was done using Webin portal, received accession number: `PRJEB75210`

### Submit samples
* Samples were copy-pasted (from excel sheet to VisualStudio) into a tsv file, [PRJEB75210-samples.tsv](./data/PRJEB75210-samples.tsv)
* Sample submission was done using Webin portal, received accession numbers: 
```
Sample	ERS19055039	CECF.1
Sample	ERS19055040	CECF.3
Sample	ERS19055041	CECF.4
Sample	ERS19055042	CES1.1
Sample	ERS19055043	CES1.2
Sample	ERS19055044	LFS2.1
Sample	ERS19055045	LFS2.4
Sample	ERS19055046	LFS2.5
Sample	ERS19055047	LFS2.7
Sample	ERS19055048	CES9.1
Sample	ERS19055049	CBT02699.1
Sample	ERS19055050	CBT02699.2
Sample	ERS19055051	CBT02699.3
Sample	ERS19055052	CBT02699.4
Sample	ERS19055053	CBT02699.5
Sample	ERS19055054	CBT02699.6
```

### Submit experiments
* Experiments were copy-pasted (from excel sheet to VisualStudio) into a tsv file, [PRJEB75210-experiments.tsv](./data/PRJEB75210-experiments.tsv)
* Experiment submission was done using Webin portal, received accession numbers: 
```
Experiment	ERX12317712	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:501-46585
Experiment	ERX12317713	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:502-46587
Experiment	ERX12317714	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:503-46589
Experiment	ERX12317715	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:503-46591
Experiment	ERX12317716	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:504-46593
Experiment	ERX12317717	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:505-46595
Experiment	ERX12317718	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:506-46597
Experiment	ERX12317719	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:507-46599
Experiment	ERX12317720	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:507-46601
Experiment	ERX12317721	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:508-46603
Experiment	ERX12317722	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:509-46605
Experiment	ERX12317723	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:509-46607
Experiment	ERX12317724	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:510-46609
Experiment	ERX12317725	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:511-46611
Experiment	ERX12317726	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:512-46613
Experiment	ERX12317727	ena-EXPERIMENT-TAB-22-04-2024-15:27:25:513-46615
Run	ERR12945371	ena-RUN-TAB-22-04-2024-15:27:25:501-46586
Run	ERR12945372	ena-RUN-TAB-22-04-2024-15:27:25:502-46588
Run	ERR12945373	ena-RUN-TAB-22-04-2024-15:27:25:503-46590
Run	ERR12945374	ena-RUN-TAB-22-04-2024-15:27:25:504-46592
Run	ERR12945375	ena-RUN-TAB-22-04-2024-15:27:25:505-46594
Run	ERR12945376	ena-RUN-TAB-22-04-2024-15:27:25:505-46596
Run	ERR12945377	ena-RUN-TAB-22-04-2024-15:27:25:506-46598
Run	ERR12945378	ena-RUN-TAB-22-04-2024-15:27:25:507-46600
Run	ERR12945379	ena-RUN-TAB-22-04-2024-15:27:25:508-46602
Run	ERR12945380	ena-RUN-TAB-22-04-2024-15:27:25:508-46604
Run	ERR12945381	ena-RUN-TAB-22-04-2024-15:27:25:509-46606
Run	ERR12945382	ena-RUN-TAB-22-04-2024-15:27:25:510-46608
Run	ERR12945383	ena-RUN-TAB-22-04-2024-15:27:25:510-46610
Run	ERR12945384	ena-RUN-TAB-22-04-2024-15:27:25:512-46612
Run	ERR12945385	ena-RUN-TAB-22-04-2024-15:27:25:513-46614
Run	ERR12945386	ena-RUN-TAB-22-04-2024-15:27:25:514-46616
```
