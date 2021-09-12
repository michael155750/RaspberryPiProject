#include "equalizeHistogrames.h"

#include "opticalFlow.h"
#include <string>


int main()
{
   
    for (size_t i = 1; i <= 3; ++i)
    {
        std::string num = std::to_string(i);
        opticalFlow("video_test" + num + ".mp4", "results.txt", "frames" + num, i);
    }
    
}
