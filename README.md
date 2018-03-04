# flownet-tests

An experiment to evaluate the effectiveness of improvements made on top of the Flownet architecture for optical flow prediction. Specifically, this project looks into:
1. Using a CRF as a post-processing step.
2. Using dilated convolutions to increase the resolution of the predictions made before upsampling.

More details to come.

## Citations
    @article{jia2014caffe,
      Author = {Jia, Yangqing and Shelhamer, Evan and Donahue, Jeff and Karayev, Sergey and Long, Jonathan and Girshick, Ross and Guadarrama, Sergio and Darrell, Trevor},
      Journal = {arXiv preprint arXiv:1408.5093},
      Title = {Caffe: Convolutional Architecture for Fast Feature Embedding},
      Year = {2014}
    }

    @article{DBLP:journals/corr/FischerDIHHGSCB15,
      author    = {Philipp Fischer and
                   Alexey Dosovitskiy and
                   Eddy Ilg and
                   Philip H{\"{a}}usser and
                   Caner Hazirbas and
                   Vladimir Golkov and
                   Patrick van der Smagt and
                   Daniel Cremers and
                   Thomas Brox},
      title     = {FlowNet: Learning Optical Flow with Convolutional Networks},
      journal   = {CoRR},
      volume    = {abs/1504.06852},
      year      = {2015},
      url       = {http://arxiv.org/abs/1504.06852},
      archivePrefix = {arXiv},
      eprint    = {1504.06852},
      timestamp = {Wed, 07 Jun 2017 14:41:04 +0200},
      biburl    = {http://dblp.org/rec/bib/journals/corr/FischerDIHHGSCB15},
      bibsource = {dblp computer science bibliography, http://dblp.org}
    }
