#===================================================================================================#
# You are very welcome to use this code. For this, clearly acknowledge                              #
# the source of this code, and cite the paper that describes the algorithm:                         #
# N. Shaul and Y. Y. Schechner, "Tomography of Turbulence Strength Based on Scintillation Imaging", #
# Proc. of European Conference on Computer Vision (ECCV), 2022.                                     #
#                                                                                                   #
# (c) Copyright Nir Shaul 2022. The python code is available for                                    #
# non-commercial use and exploration.  For commercial use contact the                               #
# author. The author is not liable for any damages or loss that might be                            #
# caused by use or connection to this code.                                                         #
#                                                                                                   #
# The code in this file is based on modification of IDS Imaging Development Systems GmbH code.      #
# from https://en.ids-imaging.com/open-source.html.                                                 #
# Modification for the use of scintillaiton imaging.												#
#===================================================================================================#

#---------------------------------------------------------------------------------------------------------------------------------------

#Libraries
from pyueye import ueye
import numpy as np
import scipy.io
import cv2
import sys
#---------------------------------------------------------------------------------------------------------------------------------------
def Capture(fileName="output8", nFrames=10, paramFile = "/home/pi/Desktop/conf.ini", sensorName = "pi0"):
    #Variables
    hCam = ueye.HIDS(0)             #0: first available camera;  1-254: The camera with the specified camera ID
    sInfo = ueye.SENSORINFO()
    cInfo = ueye.CAMINFO()
    pcImageMemory = ueye.c_mem_p()
    MemID = ueye.int()
    rectAOI = ueye.IS_RECT()
    pitch = ueye.INT()
    nBitsPerPixel = ueye.INT(24)    #24: bits per pixel for color mode; take 8 bits per pixel for monochrome
    channels = 3                    #3: channels for color mode(RGB); take 1 channel for monochrome
    m_nColorMode = ueye.INT()       # Y8/RGB16/RGB24/REG32
    bytes_per_pixel = int(nBitsPerPixel / 8)
    
    #---------------------------------------------------------------------------------------------------------------------------------------
    print("START")
    print()


    # Starts the driver and establishes the connection to the camera
    nRet = ueye.is_InitCamera(hCam, None)
    if nRet != ueye.IS_SUCCESS:
        print("is_InitCamera ERROR")

    # Reads out the data hard-coded in the non-volatile camera memory and writes it to the data structure that cInfo points to
    nRet = ueye.is_GetCameraInfo(hCam, cInfo)
    if nRet != ueye.IS_SUCCESS:
        print("is_GetCameraInfo ERROR")

    # You can query additional information about the sensor type used in the camera
    nRet = ueye.is_GetSensorInfo(hCam, sInfo)
    if nRet != ueye.IS_SUCCESS:
        print("is_GetSensorInfo ERROR")

    nRet = ueye.is_ResetToDefault( hCam)
    if nRet != ueye.IS_SUCCESS:
        print("is_ResetToDefault ERROR")

    # Set display mode to DIB
    nRet = ueye.is_SetDisplayMode(hCam, ueye.IS_SET_DM_DIB)

    # Set the right color mode
    if int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
        # setup the color depth to the current windows setting
        ueye.is_GetColorDepth(hCam, nBitsPerPixel, m_nColorMode)
        bytes_per_pixel = int(nBitsPerPixel / 8)
        print("IS_COLORMODE_BAYER: ", )
        print("\tm_nColorMode: \t\t", m_nColorMode)
        print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
        print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
        print()

    elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
        # for color camera models use RGB32 mode
        m_nColorMode = ueye.IS_CM_BGRA8_PACKED
        nBitsPerPixel = ueye.INT(32)
        bytes_per_pixel = int(nBitsPerPixel / 8)
        print("IS_COLORMODE_CBYCRY: ", )
        print("\tm_nColorMode: \t\t", m_nColorMode)
        print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
        print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
        print()

    elif int.from_bytes(sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
        # for color camera models use RGB32 mode
        m_nColorMode = ueye.IS_CM_MONO8
        nBitsPerPixel = ueye.INT(8)
        bytes_per_pixel = int(nBitsPerPixel / 8)
        print("IS_COLORMODE_MONOCHROME: ", )
        print("\tm_nColorMode: \t\t", m_nColorMode)
        print("\tnBitsPerPixel: \t\t", nBitsPerPixel)
        print("\tbytes_per_pixel: \t\t", bytes_per_pixel)
        print()

    else:
        # for monochrome camera models use Y8 mode
        m_nColorMode = ueye.IS_CM_MONO8
        nBitsPerPixel = ueye.INT(8)
        bytes_per_pixel = int(nBitsPerPixel / 8)
        print("else")

    # Can be used to set the size and position of an "area of interest"(AOI) within an image
    nRet = ueye.is_AOI(hCam, ueye.IS_AOI_IMAGE_GET_AOI, rectAOI, ueye.sizeof(rectAOI))
    if nRet != ueye.IS_SUCCESS:
        print("is_AOI ERROR")

    width = rectAOI.s32Width
    height = rectAOI.s32Height


    pParam = ueye.wchar_p()
    pParam.value = paramFile

    ueye.is_ParameterSet(hCam, ueye.IS_PARAMETERSET_CMD_LOAD_FILE, pParam, 0)
    # Prints out some information about the camera and the sensor
    print("Camera model:\t\t", sInfo.strSensorName.decode('utf-8'))
    print("Camera serial no.:\t", cInfo.SerNo.decode('utf-8'))
    print("Maximum image width:\t", width)
    print("Maximum image height:\t", height)
    print("Param File:\t\t", pParam.value)
    print()

    #---------------------------------------------------------------------------------------------------------------------------------------

    # Allocates an image memory for an image having its dimensions defined by width and height and its color depth defined by nBitsPerPixel
    nRet = ueye.is_AllocImageMem(hCam, width, height, nBitsPerPixel, pcImageMemory, MemID)
    if nRet != ueye.IS_SUCCESS:
        print("is_AllocImageMem ERROR")
    else:
        # Makes the specified image memory the active memory
        nRet = ueye.is_SetImageMem(hCam, pcImageMemory, MemID)
        if nRet != ueye.IS_SUCCESS:
            print("is_SetImageMem ERROR")
        else:
            # Set the desired color mode
            nRet = ueye.is_SetColorMode(hCam, m_nColorMode)



    # Activates the camera's live video mode (free run mode)
    nRet = ueye.is_CaptureVideo(hCam, ueye.IS_DONT_WAIT)
    if nRet != ueye.IS_SUCCESS:
        print("is_CaptureVideo ERROR")

    # Enables the queue mode for existing image memory sequences
    nRet = ueye.is_InquireImageMem(hCam, pcImageMemory, MemID, width, height, nBitsPerPixel, pitch)
    if nRet != ueye.IS_SUCCESS:
        print("is_InquireImageMem ERROR")
    else:
        print("Press q to leave the programm")

    #---------------------------------------------------------------------------------------------------------------------------------------
	############## Modification for Scintiallation Tomography ##############
    # size = (width.value, height.value)
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('video.avi', fourcc, 20.0, size)
    # Flags
    createMP4 = 0
    Visualize = 0
    createBMP = 1
    
    
    if createMP4:
        save_name = "output8.mp4"
        fps = 10
        width1 = 600
        height1 = 480
        output_size = (width1, height1)
        output_size = (width.value,height.value)
        # out = cv2.VideoWriter(save_name,cv2.VideoWriter_fourcc('M','J','P','G'), fps , output_size )
        out = cv2.VideoWriter(fileName+".mp4",
                              cv2.VideoWriter_fourcc(*'mp4v'),
                              10,
                              output_size,
                              isColor=False
                              )
    
    nFrames = int(nFrames)
    nVid    = 256
#     vid = []
#     for i in range(0,2):
#         vid.append(np.zeros((height.value, width.value,nVid),dtype = np.uint8))
    vid = np.zeros((height.value, width.value,min(nFrames,nVid)),dtype = np.uint8)

    
    idxFrame = 0
    # Continuous image display
    while(nRet == ueye.IS_SUCCESS):

        # In order to display the image in an OpenCV window we need to...
        # ...extract the data of our image memory
        array = ueye.get_data(pcImageMemory, width, height, nBitsPerPixel, pitch, copy=False)

        # bytes_per_pixel = int(nBitsPerPixel / 8)

        # ...reshape it in an numpy array...
        frame = np.reshape(array,(height.value, width.value, bytes_per_pixel))
        idxVid        = int(idxFrame/nVid)
        idxFrameInVid = idxFrame % nVid
        
        if idxFrameInVid == 0 and idxVid > 0:
            VidDic = {"V": vid, "Sensor":sensorName}
            np.save(fileName +"_"+str(idxVid-1) +".npy", vid)
#             scipy.io.savemat(fileName +"_"+str(idxVid-1) +".mat", VidDic)
            vid = np.zeros((height.value, width.value,min(nFrames-idxFrame,nVid)),dtype = np.uint8)
            print("Dump: "+fileName +str(idxVid) +".mat")
        if createBMP and ((idxFrame == 12 and nFrames >= 12 ) or (nFrames < 12 and idxFrame == 4)):
            cv2.imwrite(fileName+'.bmp',frame)
            
        
        vid[:,:,idxFrameInVid] = frame[:,:,0]
#         if idxFrame - 1 == 0: #  vid.size == 0:
#             vid = np.zeros((frame.shape[0],frame.shape[1],nFrames)) 
#             vid[:,:,0] = frame
# #             vid = frame
#         else:
# #             vid = np.concatenate((vid, frame), axis=2)
#             vid[:,:,idxFrame-1] = frame

        erase = '\x1b[1A\x1b[2K'
        print(erase)
        print(str(idxFrame+1) + ' out of ' + str(nFrames),end ="")
        

        if Visualize:
            # ...resize the image by a half
            frame = cv2.resize(frame,(0,0),fx=0.5, fy=0.5)
            #...and finally display it
            cv2.imshow("SimpleLive_Python_uEye_OpenCV", frame)
        if createMP4:   
            # out.write(frame)
            out.write(cv2.resize(frame, output_size ))
        
        idxFrame = idxFrame + 1
        # Press q if you want to end the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if idxFrame+1 > nFrames:
            break

    #---------------------------------------------------------------------------------------------------------------------------------------

    # Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
    ueye.is_FreeImageMem(hCam, pcImageMemory, MemID)

    # Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
    ueye.is_ExitCamera(hCam)

    # Destroys the OpenCv windows
    if Visualize: cv2.destroyAllWindows()
    if createMP4: out.release()
    
    VidDic = {"V": vid, "Sensor":sensorName}
#     scipy.io.savemat(fileName +"_"+str(idxVid) +".mat", VidDic)
    np.save(fileName +"_"+str(idxVid) +".npy", vid)

    print()
    print("END")
    
# Capture("Test2" + "_"+ "1",10)
