
There are 5 files included in the tar file:

 1 - 'annotated_sentences.tar' contains the sentences as presented to
the annotators. Every line in this file contains a key that links with
the tags given by the annotators that are stored in the second file.

example:
bank.n.Sports.186  bank ? 16 The judge noted that Segers had lied to police about money he paid into his swiss bank account and Grobbelaar had lied about money he paid to Vincent . 


 2 - 'gold_standard_EMNLP05.txt' contains the tags given by the
 annotators. This is the data set that was used for the results given
 in the EMNLP'05 paper.

example:
| bank.n.Sports.186          | bank%1:14:00::                         |
| bank.n.Sports.186          | bank%1:14:00::                         |
| bank.n.Sports.186          | bank%1:14:00::                         |


 3 - 'gold_standard_clean.txt' is an updated version of the second
file. Some errors still present in the second file, were removed in
the third (hence the 'clean' extension to the file-name).  Notes on
the cleaning up process are added at the bottom of this readme.

 4 - 'results_0103.txt' is an overview of the number of usable
sentences per target word. Ideally this would be 300 (100 BNC, 100
Sports, 100 Finance). The first table shows the number of sentences
per target word for which at least two annotators agree. This is the
case for almost every word.  The second table shows the number of
_usable_ sentences. That is, the number of sentences for which (at
least) two annotators agree, but excluding the ones that are tagged
'unclear' or 'unlisted-sense'.  (Note that these figures are
pre-cleaning)

 5 - A pdf version of the EMNLP'05 paper. It explains in some detail
 how the annotating task was set up.



Some notes on the data: (these notes were for the pre-cleaning data;
some of the issues are solved in the post-cleaning data)

 - You can see that there are a few words (most notably 'pitch'
and 'will') that are problematic. Most 'unlisted-senses' of 'will' are
cases where 'will' is mis-tagged as a noun (should be verb).

 - For 'pitch' there are quite a few cases where 'pitch' is not
   recognised as being part of the multi-word 'fever pitch'.

 - Other 'unlisted-sense' case are genuine: the (in UK English often
   used) 'play field' meaning of pitch is missing in WordNet 1.7.1

 - There are also cases where the annotator ticked two boxes instead
of one (as they were instructed to do). These look like:
bill%1:10:04::__bill%1:10:06:: (i.e. seperated by a double underscore)




Notes on cleaning up the data:

Three types of errors were removed from the data. I give a few
examples of each error. The list of examples is not
exhaustive. A complete list can be generated on request.

 - removed sentences in which the target word is part of a generally
   used multi-word expression.
   E.g.: 'bank holiday' (It will run until 6 pm each day over the bank
         holiday, and to 5 pm on Tuesday.)
       : 'blue chip'
       : 'pitch' (Tension between the two countries rose to fever
         pitch in 1994 when Athens deported thousands of albanian
         immigrants following Tirana's deportation of a senior greek
         cleric.)

 - removed sentences in which the target word is a Proper Name (and
   wasn't recognized as such by the PoS tagger).
   E.g.: 'bill' (The bills led 3-0 midway through the first quarter on
         a 31-yard field goal by Steve Christie.)
       : 'fan' ("There is a broad consensus on a need to stimulate the
         economy," said fan gang, an economist and director of the
         China reform foundation, an authoritative think-tank.)
       : 'will'

 - removed sentences where the target word is mistagged as a Noun
   (should have been a Verb mostly).
   E.g.: 'bond' ('We could n't find anyone to bond us in time,' says
         Mrs Burrows.)
       : 'check' (I meet these guys who are six years younger than me
         and they 're going, 'You gotta check out The Doors, man'.)
       : 'fan' (The communist speaker of the Duma, Gennady Seleznyov,
         warned that the liberal team now in charge of economic policy
         could fan social tensions in Russia.)
       : 'phase'
       : 'right' ('My goodness, Eccles,' said Derek, flattening his
         hair, 'I believe you may have hit the nail right on the
         knuckle.)




