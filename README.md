# GPT-4V(ision) is a Generalist Web Agent, if Grounded

Code, Dataset, and Demo for the paper "[GPT-4V(ision) is a Generalist Web Agent, if Grounded](https://github.com/OSU-NLP-Group/SeeAct/blob/gh-pages/static/paper/SeeAct_Paper.pdf)".

Check [project website](https://osu-nlp-group.github.io/SeeAct/) for an overview and demo videos.

Release process:
- [ ] Dataset
  - [x] Example data for the three element grounding methods
  - [ ] Data used in the paper with screenshot images
- [x] Code
  - [x] Offline Experiments
    - [x] Screenshot generation
    - [x] Code to overlay image annotation
    - [ ] BLIP-2 fine-tuning
  - [ ] Online Evaluation Tool
- [ ] Models
  - [ ] Fine-tuned BLIP-2 Model


## Dataset
The dataset is derived from Mind2Web by pairing each HTML text with the rendered webpage screenshots. 
The screenshot image data comes from the [Raw Dump with Full Traces and Snapshots](https://github.com/OSU-NLP-Group/Mind2Web?tab=readme-ov-file#raw-dump-with-full-traces-and-snapshots) captured with PlayWright during data annotation.


## Screenshot Generation
These scripts can collect screenshot images from the Mind2Web raw dump and overlay image annotation for action grounding.


## Online Evaluation Tool
We develop a new online evaluation tool using Playwright to evaluate web agents on live websites. Our tool can convert the predicted action into a browser event and execute it on the website. 


We acknowledge Xiang Deng for his initial contribution to this tool. 



## Contact

Questions or issues? File an issue or contact [Boyuan Zheng](https://boyuanzheng010.github.io/)


## Licensing Information
The code under this repo is licensed under an MIT License.

## Disclaimer

The code was released solely for research purposes, with the goal of making the web more accessible via language technologies. The authors are strongly against any potentially harmful use of the data or technology by any party. 

