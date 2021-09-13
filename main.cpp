
#include "opticalFlow.h"
#include <string>




    
    
    

int main(int argc, char **argv)
{
    std::string videoName = argv[1];
    std::string textFileName = argv[2];
    std::string imageFolderName = argv[3];
    std::string bedNumber = argv[4];

    childrenRec(videoName, textFileName, imageFolderName, std::stoi(bedNumber));
    return 0;
}