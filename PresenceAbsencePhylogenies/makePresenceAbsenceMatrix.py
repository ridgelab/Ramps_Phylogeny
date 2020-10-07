#! /usr/bin/env python
#This program will go through all of the aligned fasta files in the directory.
#It will then create a supermatrix of all of the concatenated orthologs, inserting a '?' where the ortholog is unknown
import sys
import os
import argparse

def parseArgs():
        '''
        Argument parsing is done.
        Required to have an input file.
        '''
        parser = argparse.ArgumentParser(description='Create Supermatrix.')
        #parser.add_argument("-t",help="Number of Cores",action="store",dest="threads",default=0,type=int, required=False)
        parser.add_argument("-id",help="Input Directory with Ortholog Fasta Files",action="store", dest="inputDir", required=True)
        parser.add_argument("-it",help="Input Table of Genes",action="store", dest="inputTable", required=True)
        parser.add_argument("-iq",help="Input Quantile File",action="store", dest="inputQuantile", required=True)
        parser.add_argument("-tnt",help="Output TNT File Path",action="store",dest="outputTNT", required=False)
        parser.add_argument("-iqtree",help="Output IQtree File Path",action="store",dest="outputIQTree",required=False)
        parser.add_argument("-k",help="Keyfile containing column number and gene name",action="store",dest="outputKey",required=False)
        args = parser.parse_args()
        
        return args


def filterGenesAndSpecies(genelist,geneToFreq,specieslist,speciesToGenes):
        #print("Filtering")
        needsUpdate = False
        genesToDelete = []
        for gene in genelist:
                if geneToFreq[gene] < len(specieslist) * 0.05:  #Is the gene found in < 5% of all the species?
                        genelist.remove(gene)
                        del geneToFreq[gene]
                        needsUpdate = True
                        genesToDelete.append(gene)

        for species in specieslist:
                #print speciesToGenes[species]
                for gene in genesToDelete:
                        if gene in speciesToGenes[species]:
                                speciesToGenes[species].remove(gene)
                                needsUpdate = True
        #        print("Comparing ",len(speciesToGenes[species]), " to ", len(genelist))
                if len(set(speciesToGenes[species]).intersection(set(genelist))) < len(genelist) * 0.05: #Does our species have at least 5% of all the genes?
        #                print("Removing ", species)
        #                print "species to genes ", speciesToGenes[species]
                        for g in speciesToGenes[species]:
                                #print "genetofreq[g]:", geneToFreq[g]
                                if g not in geneToFreq:
                                        pass
                                elif geneToFreq[g] <= 1:
                                        del geneToFreq[gene]
                                else:
                                        geneToFreq[g] -= 1
                        specieslist.remove(species)
                        del speciesToGenes[species]
                        needsUpdate = True

        
        if needsUpdate:
                genelist,geneToFreq,specieslist,speciesToGenes = filterGenesAndSpecies(genelist,geneToFreq,specieslist,speciesToGenes)
        return genelist,geneToFreq,specieslist,speciesToGenes

def writeOutputFiles(args,genelist,genes,specieslist,orthosToSpecies):
        if args.outputTNT:        
                outTNTfile = open(args.outputTNT,"w")
        if args.outputIQTree:
                outIQTreefile = open(args.outputIQTree,"w")
        if args.outputKey:
                outputKeyfile = open(args.outputKey,"w")
                outputKeyfile.write("Column,Gene\n")
                column = 0
                for gene in genelist:
                        if args.outputKey:
                            outputKeyfile.write(str(column) + "," + gene + "\n")

                        column += 1
        
#        totalChars = 0
#        for gene in genelist:
#                totalChars += genes[gene]["size"]

        if args.outputTNT:
                outTNTfile.write("xread\n")
                outTNTfile.write(str(len(genelist)) + " " + str(len(specieslist))  + "\n")
        if args.outputIQTree:
                outIQTreefile.write(str(len(specieslist)) + " " + str(len(genelist)) + "\n")

        qfile = open(args.outputQuantile,"w")
        top_5 = qfile.readline().strip().split(",")

        #print(genes)
        matrix = ""
        for species in specieslist:
                matrix += species + "\t"
                for gene in genelist:
                        if gene not in top_5:
                                continue
                        if species in genes[gene]:
                                matrix += "1" #genes[gene][species]
                        elif species not in orthosToSpecies[gene]:
                            matrix += "?"
                        else:
                                matrix += "0"
                                #for s in range(genes[gene]["size"]):
                                #        matrix += "?"
                        #        outfile.write("\t")

                matrix += "\n"

        if args.outputTNT:
                outTNTfile.write(matrix)
                outTNTfile.write(";\n\n\nproc /;\ncomments 0\n;")
                outTNTfile.close()
        if args.outputIQTree:
                outIQTreefile.write(matrix)
                outIQTreefile.close()
        if args.outputKey:
                outputKeyfile.close()
        
        
        #print "geneToFreq: ", geneToFreq
        #print "speciesToGenes: ", speciesToGenes



def readInputFiles(args,orthosToSpecies): 
        genes = {} 
        specieslist = []
        genelist = []
        geneToFreq = {}
        speciesToGenes = {}
        for r, d, f in os.walk(args.inputDir):
                for filename in f:
                        if "aligned" in filename:
                                inFile = open(os.path.join(r,filename))
                                header = inFile.readline()
                                while header != "":
                                        fields = header.split("__")
                                        if len(fields) == 1:
                                                break
                                        geneName = fields[1]
                                        species = fields[0]
                                        species = species[1:]
                                        if species not in specieslist: #Makes our list of all species and initializes element in species to gene dictionary
                                                specieslist.append(species)
                                                speciesToGenes[species] = []
                                        if geneName not in genelist: #Makes our list of all genes and initializes element in get to freq dictionary
                                                genelist.append(geneName)
                                                geneToFreq[geneName] = 0
        
                                        line = inFile.readline()
                                        seq = ""
                                        while line != "" and line[0] != ">":
                                                seq += line.strip()
                                                line = inFile.readline()
                                
                                        if geneName not in genes: #This will execute for the first line of each aligned file. Initialize element in genes dictionary, mark the size of the gene.
                                                genes[geneName] = {species:seq}
                                                genes[geneName]["size"] = len(seq)
                                                geneToFreq[geneName] += 1
                                        if species not in genes[geneName]: #For the first ortholog of the species
                                                genes[geneName][species] = seq
                                                geneToFreq[geneName] += 1
                                                speciesToGenes[species].append(geneName)
                                        else: #In case the species had multiple of the same sequence, choose the longer one.
                                                if seq.count('_') < genes[geneName][species].count('_'):
                                                        genes[geneName][species] = seq
                                        header = line
                                        if "Dummy" in header:
                                                #print "Dummy"
                                                break
#        print "species to genes: ", speciesToGenes
        csvLine = args.inputDir + ","
        csvLine +=  str(len(genelist)) + ","
        csvLine +=  str(len(specieslist)) + ","
        genelist,geneToFreq,specieslist,speciesToGenes = filterGenesAndSpecies(genelist,geneToFreq,specieslist,speciesToGenes)
        csvLine +=  str(len(genelist)) + ","
        csvLine +=  str(len(specieslist))
        print csvLine
        #print "Number of genes: ", len(genelist)
        #print "Number of species: ", len(specieslist)
#        print "species to genes: ", speciesToGenes
#        print "Genes: ", genelist
        writeOutputFiles(args,genelist,genes,specieslist,orthosToSpecies)

def makeOrthoDic(args):
    table = open(args.inputTable,"r")
    orthosToSpecies = {}
    for line in table:
        fields = line.split()
        gene = fields[0]
        species = fields[1]
        if gene not in orthosToSpecies:
            orthosToSpecies[gene] = [species]
        else:
            if species not in orthosToSpecies[gene]:
                orthosToSpecies[gene].append(species)
    print("Number of orthologs: ", len(orthosToSpecies))
    return orthosToSpecies
        
if __name__ =='__main__':
        '''
        Main.
        '''
        args = parseArgs()
        orthosToSpecies = makeOrthoDic(args)
        readInputFiles(args,orthosToSpecies)

