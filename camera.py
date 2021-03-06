from picamera import PiCamera
import logging
import string

import config as cfg
import utils


class Camera():
    ''' #TODO
    '''
    
    def __init__(self):
        ''' #TODO
        '''
        
        #: PiCam setup
        self.cam = PiCamera()
        self.cam.resolution = (1280, 720)
        
        #: init logger
        self.logger = logging.getLogger(__name__)
        
        #: init variables
        self.is_recording = False
        self.rec_extension = cfg.CAMERA_RECORDING_FORMAT
        self.convert_extension = cfg.CAMERA_CONVERTING_FORMAT
        self.video_dir = '{path}/{directory}'.format(path = cfg.FILE_PATH, directory = cfg.VIDEO_DIR)

    def start_recording(self) -> None:
        ''' #TODO
        '''
        
        #: Only start if camera is currently not active
        if not self.is_recording:
            
            #: Set video name
            self.video_name = utils.timestring()
            
            #: Start PiCamera recording
            self.is_recording = True
            self.cam.start_recording(self._get_video_path(self.video_name, self.rec_extension))
            self.logger.debug('recording started: {}'.format(self.video_name + self.rec_extension))
        
    def stop_recording(self) -> str:
        ''' #TODO
        '''

        if self.is_recording:
            
            #: save name in case a new video with different name starts during conversion
            self.converting_name = self.video_name

            #: Stop PiCamera recording
            self.cam.stop_recording()
            self.logger.debug('recording stopped: {}'.format(self.converting_name + self.convert_extension))
            self.is_recording = False
            self._convert()
            return self._get_video_path(self.converting_name, self.convert_extension)
        
        return None
    
    def _get_video_path(self, name: str, extension: str) -> str:
        ''' #TODO
        '''

        return '{folder}/{name}{extension}'.format(folder = self.video_dir, name = name, extension = extension)
        
    def _convert(self) -> None:
        ''' Converts video captured by PiCamera in known format and deletes old video
        '''
        
        #: Get current filename, and filename after converting
        before = self._get_video_path(self.converting_name, self.rec_extension)
        after  = self._get_video_path(self.converting_name, self.convert_extension)
        
        #: Convert command (with semicolon to concatenate)
        convert = 'MP4Box -add {before} {after};'.format(before = before, after = after)
        
        #: Delete command
        delete = ' rm {file}'.format(file=before)
        
        #: Execute both
        utils.shell_cmd(convert + delete)
        self.logger.debug('convert and delete video')
        
        
