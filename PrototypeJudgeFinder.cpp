//  JudgeFinder
//
//  Created by Dongpeng Xia on 2/29/16.

//assumptions: all english files, all plaintext, all have judges contained in same part of file


#include <iostream>
#include <fstream>
#include <string>

using namespace std;

void loadFileFindJudges(string);

int main(int argc, const char * argv[])
{
    string fName;
    
    string listOfFiles = "/Users/dongpengxia/Documents/CS/JudgesChallenge/FileNames.txt";
    ifstream inFile;
    inFile.open(listOfFiles.c_str());
    if (!inFile)
    {
        cout << "Data file failed to open" << endl;
        cout << listOfFiles << endl;
    }
    else
    {
        while(!inFile.eof())
        {
            getline(inFile,fName);
            loadFileFindJudges(fName);
        }
    }
    
    return 0;
}//end main


/***************************************************************
*                                                              *
*                  loadFileFindJudges                          *
*                                                              *
* Description: stand-alone function opens fileNameAndPath,     *
* then searches it for the names of judges, which are output   *
*                                                              *
***************************************************************/

void loadFileFindJudges(string fileNameAndPath)
{
    
    ifstream inFileStream;
    
    //Open file name and path
    inFileStream.open(fileNameAndPath.c_str());
    
    //If the input data file failed to open
    if (!inFileStream)
    {
        cout << "Data file failed to open" << endl;
        cout << fileNameAndPath << endl;
    }
    else
    {
        //File open confirmation message
        cout << "Data file opened successfully for reading:" << endl;
        cout << fileNameAndPath << endl;
        
        
        //flag for whether judges have been found
        bool foundJudges = false;
        
        //stores contents of line of text in a string
        string lineContent = "";
        
        //while the file still has content to read and judges have not been found
        while(!inFileStream.eof() && !foundJudges)
        {
            //store next line into lineContent
            getline(inFileStream, lineContent);
            
            //if lineContent contains "The European Court of Human Rights"
            if((lineContent.find("The European Court of Human Rights")) != string::npos)
            {
                //get next line, expected to contain president's name
                getline(inFileStream, lineContent);
                
                //if lineContent contains "President"
                if(lineContent.find("President") != string::npos)
                {
                    //processes and updates lineContent until it contains "judges"
                    while(lineContent.find("judges") == string::npos)
                    {
                        getline(inFileStream, lineContent);
                        cout << lineContent;
                    }
                    cout << endl << endl;
                    
                    foundJudges = true;
                    
                }//end if
            }//end if
        }//end while
    }//end else
    
}//end loadFiles