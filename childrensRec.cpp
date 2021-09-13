#include "childrensRec.h"
#include <fstream>
#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/video.hpp>
#include <ctime>
#include <chrono>

using namespace cv;
using namespace std;
    /**
     * @return string of the time now as day date hour and year 
    */
    string timeNow()
    {
        char *buffer = new char[30];
        auto now = chrono::system_clock::now();
        auto epoch = chrono::system_clock::to_time_t(now);

        ctime_s(buffer, 30, &epoch);
        string result = buffer;
        delete[]buffer;
        return result;
    }

    /**
     * @brief save the time and bed number in resultFile and the images from prev_frames in framesFolder
     * @param resultsFile path to a text file
     * @param bedNumber 
     * @param prev_frames a vector of images
     * @param framesFolder a path to folder for the images
    */
    void saveTimeImages(std::string &resultsFile, int bedNumber, std::vector<cv::Mat> &prev_frames, std::string &framesFolder)
    {
        ofstream fout;
        fout.open(resultsFile, ios::app);


        string time = timeNow();

        fout << "time: " << time << "bedNumber: " << bedNumber << endl;

        fout.close();

        for (size_t i = 0; i < prev_frames.size(); ++i)
        {
            imwrite(framesFolder + "\\bed" + to_string(bedNumber) + "-frame" + to_string(i) +  ".png", prev_frames[i]);
        }
    }

    /**
     * @brief Find move character go out of the frame and save 10 images before the moment.
     *
     * @param resultsFile path to a text file
     * @param bedNumber 
     * @param prev_frames a vector of images
     * @param framesFolder a path to folder for the images
     * @return 
    */
    void childrenRec(string videoFile, string resultsFile, string framesFolder, int bedNumber)
    {

        VideoCapture capture(videoFile);
        if (!capture.isOpened())
        {
            //error in opening the video input
            cerr << "Unable to open file!" << endl;
            return;
        }

        Mat old_frame, old_gray;
        vector<Point2f> good_points, calc_points, good_points_no_frame;
        const int outer_frame_size = 200;
        const int outer_capture_frame_size = 10;
        const int max_size_frame_vector = 10;
        
        // Take first frame, equlize colors and find corners in it
        capture >> old_frame;
        cvtColor(old_frame, old_gray, COLOR_BGR2GRAY);
        equalizeHist(old_gray, old_gray);
        goodFeaturesToTrack(old_gray, good_points, 100, 0.1, 7, Mat(), 7, false, 0.04);

        for (auto it = good_points.begin(); it != good_points.end(); ++it) {
            if (!(it->x > old_gray.cols - outer_frame_size || it->x < outer_frame_size ||
                it->y > old_gray.rows - outer_frame_size || it->y < outer_frame_size))
                good_points_no_frame.push_back(*it);
        }
        if (good_points_no_frame.empty())
        {
            cout << ("nothing to show!\n");
            return;
        }

        vector<Mat> prev_frames;
        while (true) {
            Mat frame, frame_gray;
            capture >> frame;

            prev_frames.push_back(frame);
            if (frame.empty())
                break;
            cvtColor(frame, frame_gray, COLOR_BGR2GRAY);
            // calculate optical flow
            vector<uchar> status;
            vector<float> err;
            TermCriteria criteria = TermCriteria((TermCriteria::COUNT)+(TermCriteria::EPS), 10, 0.03);
            equalizeHist(frame_gray, frame_gray);
            calcOpticalFlowPyrLK(old_gray, frame_gray, good_points_no_frame, calc_points, status, err, Size(15, 15), 2, criteria);
            vector<Point2f> good_new;
            
            for (uint i = 0; i < good_points_no_frame.size(); ++i)
            {
                // Select good points
                if (status[i] == 1) {
                    good_new.push_back(calc_points[i]);

                    //find the character get out of image by points
                    if (calc_points[i].x > frame_gray.cols - outer_capture_frame_size || calc_points[i].x < outer_capture_frame_size ||
                        calc_points[i].y > frame_gray.rows - outer_capture_frame_size || calc_points[i].y < outer_capture_frame_size) {

                        saveTimeImages(resultsFile, bedNumber, prev_frames, framesFolder);
                        return;
                    }
                }

            }

            //fill the previous frames vector to maximum size
            if (prev_frames.size() > max_size_frame_vector - 1) {
                prev_frames.erase(prev_frames.begin());
            }



            // Now update the previous frame and previous points
            old_gray = frame_gray.clone();
            good_points_no_frame = good_new;
        }
    }

