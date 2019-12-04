#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 19:53:42 2019

@author: usingh
contains classes of RNA-Seq mapping programs
"""

from pyrpipe.myutils import *

class Aligner:
    def __init__(self):
        self.category="Alignement"
        self.passedArgumentDict={}
    
    def performAlignment(self):
        pass

class Hisat2:
    def __init__(self,hisat2Index="",**kwargs):
        """HISAT2 constructor. Initialize hisat2's index and other parameters.
        Parameters
        ----------
        hisat2Index string
            path to q histat2 index (note -x is ommited from validArgsList). This index will be used when hisat is invoked.
        dict
            parameters passed to the hisat2 program. These parameters could be overridden later when running hisat.
        ----------
        
        """ 
        super().__init__() 
        self.programName="hisat2"
        #check if hisat2 exists
        if not checkDep([self.programName]):
            raise Exception("ERROR: "+ self.programName+" not found.")
        
        self.validArgsList=['-x','-1','-2','-U','--sra-acc','-S','-q','--qseq','-f','-r','-c','-s',
                            '-u','-5','-3','--phred33','--phred64','--int-quals',
                            '--sra-acc','--n-ceil','--ignore-quals','--nofw','--norc','--pen-cansplice',
                            '--pen-noncansplice','--pen-canintronlen','--pen-noncanintronlen','--min-intronlen'
                            ,'--max-intronlen','--known-splicesite-infile','--novel-splicesite-outfile',
                            '--novel-splicesite-infile','--no-temp-splicesite','--no-spliced-alignment',
                            '--rna-strandness','--tmo','--dta','--dta-cufflinks','--avoid-pseudogene',
                            '--no-templatelen-adjustment','--mp','--sp','--no-softclip','--np','--rdg',
                            '--rfg','--score-min','-k','-I','-X','--fr','--rf','--ff','--no-mixed',
                            '--no-discordant','-t','--un','--al','--un-conc','--al-conc','--un-gz',
                            '--summary-file','--new-summary','--quiet','--met-file','--met-stderr',
                            '--met','--no-head','--no-sq','--rg-id','--rgit-sec-seq','-o','-p',
                            '--reorder','--mm','--qc-filter','--seed','--non-deterministic',
                            '--remove-chrname','--add-chrname','--version']
        
        
        #initialize the passed arguments
        self.passedArgumentDict=kwargs
        
        #if index is passed, update the passed arguments
        if len(hisat2Index)>0 and checkHisatIndex(hisat2Index):
            print("HISAT2 index is: "+hisat2Index)
            self.hisat2Index=hisat2Index
            self.passedArgumentDict['-x']=self.hisat2Index
        else:
            print("No Hisat2 index provided. Please build index now to generate an index using buildHisat2Index()....")
            
        
        
            
    def buildHisat2Index(self,indexPath,indexName,*args,**kwargs):
        """Build a hisat index with given parameters and saves the new index to self.hisat2Index.
        Parameters
        ----------
        arg1: string
            Path where the index will be created
        arg2: string
            A name for the index
        arg3: tuple
            Path to reference input files
        arg4: dict
            Parameters for the hisat2-build command
        
        Returns
        -------
        bool:
            Returns the status of hisat2-build
        """
        overwrite=True
        print("Building hisat index...")
        
        hisat2BuildValidArgsList=['-c','--large-index','-a','-p','--bmax','--bmaxdivn','--dcv','--nodc','-r','-3','-o',
                                  '-t','--localoffrate','--localftabchars','--snp','--haplotype','--ss','--exon',
                                  '--seed','-q','-h','--usage','--version']
        #create the out dir
        if not checkPathsExists(indexPath):
            if not mkdir(indexPath):
                print("ERROR in building hisat2 index. Failed to create index directory.")
                return False
        
        if not overwrite:
            #check if files exists
            if checkHisatIndex(os.path.join(indexPath,indexName)):
                print("Hisat2 index with same name already exists. Exiting...")
                return False
        
        hisat2Build_Cmd=['hisat2-build']
        #add options
        hisat2Build_Cmd.extend(parseUnixStyleArgs(hisat2BuildValidArgsList,kwargs))
        #add input files
        hisat2Build_Cmd.append(str(",".join(args)))
        #add dir/basenae
        hisat2Build_Cmd.append(os.path.join(indexPath,indexName))
        print("Executing:"+str(" ".join(hisat2Build_Cmd)))
        
        #start ececution
        log=""
        try:
            for output in executeCommand(hisat2Build_Cmd):
                print (output)    
                log=log+str(output)
            #save to a log file

        except subprocess.CalledProcessError as e:
            print ("Error in command...\n"+str(e))
            #save error to error.log file
            return ""
        
        #check if sam file is present in the location directory of sraOb
        if not checkHisatIndex(os.path.join(indexPath,indexName)):
            print("ERROR in building hisat2 index.")
            return False
        
        #set the index path
        self.hisat2Index=os.path.join(indexPath,indexName)
        self.passedArgumentDict['-x']=self.hisat2Index
        
        #return the path to output sam
        return True
        
        
    def performAlignment(self,sraOb,outSamSuffix="_hisat2",**kwargs):
        """Function to perform alignment using self object and the provided sraOb.
        
        Parameters
        ----------
        arg1: SRA object
            An object of type SRA. The path to fastq files will be obtained from this object.
        arg2: string
            Suffix for the output sam file
        arg3: dict
            Options to pass to hisat2.
        """
        
        
        #create path to output sam file
        outSamFile=os.path.join(sraOb.location,sraOb.srrAccession+outSamSuffix+".sam")
        
        """
        Handle overwrite
        """
        overwrite=True
        if not overwrite:
            #check if file exists. return if yes
            if os.path.isfile(outSamFile):
                print("The file "+outSamFile+" already exists. Exiting..")
                return outSamFile
        
        #find layout and fq file paths
        if sraOb.layout == 'PAIRED':
            newOpts={"-1":sraOb.localfastq1Path,"-2":sraOb.localfastq2Path,"-S":outSamFile}
        else:
            newOpts={"-U":sraOb.localfastqPath,"-S":outSamFile}
        
        #add input files to kwargs, overwrite kwargs with newOpts
        mergedOpts={**kwargs,**newOpts}
        
        #call runHisat2
        status=self.runHisat2(**mergedOpts)
        
        if status:
            #check if sam file is present in the location directory of sraOb
            if checkFilesExists(outSamFile):
                return outSamFile
        else:
            return ""
            
        
    def runHisat2(self,**kwargs):
        """Wrapper for running hisat2.
        Run HISAT2 using and SRA object and produce .bam file as result. The HISAT2 index used will be self.hisat2Index.
        All output will be written to SRA.location by default.
        
        Parameters
        ----------
        arg1: dict
            arguments to pass to hisat2. This will override parametrs already existing in the self.passedArgumentList list but NOT replace them.
            
        Returns
        -------
        bool:
                Returns the status of hisat2. True is passed, False if failed.
        """
        
        #check for a valid index
        if not self.checkHisat2Index():
            raise Exception("ERROR: Invalid HISAT2 index. Please run build index to generate an index.")
            
        #override existing arguments
        mergedArgsDict={**self.passedArgumentDict,**kwargs}
       
        hisat2_Cmd=['hisat2']
        #add options
        hisat2_Cmd.extend(parseUnixStyleArgs(self.validArgsList,mergedArgsDict))        
        
        print("Executing:"+" ".join(hisat2_Cmd))
        
                
        #start ececution
        log=""
        try:
            for output in executeCommand(hisat2_Cmd):
                #print (output)    
                log=log+str(output)
            #save to a log file
            
        except subprocess.CalledProcessError as e:
            print ("Error in command...\n"+str(e))
            #save error to error.log file
            return False        
        #return status
        return True
        
        
    
    def checkHisat2Index(self):
        if hasattr(self,'hisat2Index'):
            return(checkHisatIndex(self.hisat2Index))
        else:
            return False

    



class Star:
    def __init__(self,starIndex):
        """STAR constructor. Initialize star's index and other parameters.
        """
        
        
        super().__init__() 
        self.programName="star"
        
        self.validArgsList=[]
        self.depList=[self.programName]        
        #check if hisat2 exists
        if not checkDep(self.depList):
            raise Exception("ERROR: "+ self.programName+" not found.")
            
            
            
    def performAlignment(self,sraOb,outSamSuffix="_star",**kwargs):
        """Function to perform alignment using self object and the provided sraOb.
        
        Parameters
        ----------
        arg1: SRA object
            An object of type SRA. The path to fastq files will be obtained from this object.
        arg2: string
            Suffix for the output sam file
        arg3: dict
            Options to pass to hisat2.
        """
        
        pass
            

class Bowtie2(Aligner):
    def __init__(self,bowtie2Index):
        """Bowtie2 constructor. Initialize star's index and other parameters.
        """       
        
        super().__init__() 
        self.programName="bowtie2"
        
        self.validArgsList=[]
        self.depList=[self.programName]        
        #check if hisat2 exists
        if not checkDep(self.depList):
            raise Exception("ERROR: "+ self.programName+" not found.")
        
        
        self.bowtie2Index=bowtie2Index
    
    
    def performAlignment(self,sraOb,outSamSuffix="_star",**kwargs):
        """Function to perform alignment using self object and the provided sraOb.
        
        Parameters
        ----------
        arg1: SRA object
            An object of type SRA. The path to fastq files will be obtained from this object.
        arg2: string
            Suffix for the output sam file
        arg3: dict
            Options to pass to hisat2.
        """
        
        pass
    
    def runBowTie2(self,sraOb,**kwargs):
        """Function to run bowtie2
        """
        outDir=sraOb.location
        outSamFile=os.path.join(outDir,"bt2.sam")
        unmapFname=os.path.join(outDir,sraOb.srrAccession+"norRNA.fastq")
        
        bowtie2_Cmd=[self.programName]
        bowtie2_Cmd.extend(["-p","10","--norc","-x",self.bowtie2Index,"-S",outSamFile,"--un",unmapFname,"-U",sraOb.localfastqPath])
        
        print("Executing:"+" ".join(bowtie2_Cmd))
        
        #start ececution
        log=""
        try:
            for output in executeCommand(bowtie2_Cmd):
                print (output)    
                log=log+str(output)
            #save to a log file
            
        except subprocess.CalledProcessError as e:
            print ("Error in command...\n"+str(e))
            #save error to error.log file
            return ""
        
        return unmapFname
        
    
    
    
