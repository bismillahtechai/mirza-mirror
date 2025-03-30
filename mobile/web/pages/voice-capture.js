import React, { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import { uploadVoiceRecording } from '../api/apiService';

const VoiceCapture = () => {
  const router = useRouter();
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioBlob, setAudioBlob] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);
  
  useEffect(() => {
    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
      
      if (mediaRecorderRef.current && isRecording) {
        mediaRecorderRef.current.stop();
      }
    };
  }, [isRecording]);
  
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        setAudioBlob(audioBlob);
        
        // Stop all tracks to release the microphone
        stream.getTracks().forEach(track => track.stop());
      };
      
      // Start recording
      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);
      setError(null);
      
      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 100);
      }, 100);
      
    } catch (err) {
      console.error('Error accessing microphone:', err);
      setError('Could not access microphone. Please check permissions and try again.');
    }
  };
  
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
  };
  
  const handleUpload = async () => {
    if (!audioBlob) return;
    
    try {
      setIsUploading(true);
      setError(null);
      
      await uploadVoiceRecording(audioBlob);
      router.push('/');
      
    } catch (err) {
      console.error('Error uploading recording:', err);
      setError('Failed to upload recording. Please try again.');
      setIsUploading(false);
    }
  };
  
  const formatTime = (timeInMs) => {
    const totalSeconds = Math.floor(timeInMs / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    const tenths = Math.floor((timeInMs % 1000) / 100);
    
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${tenths}`;
  };
  
  return (
    <div className="min-h-screen bg-neutral-50">
      <Head>
        <title>Voice Capture | Mirza Mirror</title>
        <meta name="description" content="Record a voice note for Mirza Mirror" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-neutral-900">Voice Capture</h1>
            <button
              onClick={() => router.back()}
              className="text-neutral-600 hover:text-neutral-900"
            >
              Cancel
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white shadow-sm rounded-lg p-6 flex flex-col items-center">
          {error && (
            <div className="mb-6 p-3 bg-red-50 text-red-700 rounded-md w-full">
              {error}
            </div>
          )}
          
          <div className="mb-8 text-center">
            {isRecording ? (
              <>
                <div className="text-2xl font-bold text-red-600 mb-2">Recording...</div>
                <div className="text-3xl font-mono">{formatTime(recordingTime)}</div>
                
                {/* Waveform visualization */}
                <div className="flex items-end justify-center h-16 space-x-1 mt-4">
                  {Array.from({ length: 20 }).map((_, i) => (
                    <div 
                      key={i}
                      className="w-1.5 bg-red-500 rounded-full animate-pulse"
                      style={{ 
                        height: `${Math.random() * 50 + 10}%`,
                        animationDelay: `${i * 0.05}s`
                      }}
                    />
                  ))}
                </div>
              </>
            ) : (
              <>
                <div className="text-6xl text-primary-500 mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-24 w-24 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  </svg>
                </div>
                <div className="text-xl text-neutral-700">
                  {audioBlob ? 'Recording complete' : 'Tap to start recording'}
                </div>
              </>
            )}
          </div>
          
          {audioBlob && !isRecording && (
            <div className="mb-6 w-full">
              <audio 
                controls 
                src={URL.createObjectURL(audioBlob)} 
                className="w-full"
              />
            </div>
          )}
          
          <div className="flex space-x-4">
            {isRecording ? (
              <button
                onClick={stopRecording}
                className="w-16 h-16 rounded-full bg-red-600 text-white flex items-center justify-center hover:bg-red-700 transition-colors"
                aria-label="Stop recording"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
                </svg>
              </button>
            ) : (
              <>
                {!audioBlob ? (
                  <button
                    onClick={startRecording}
                    className="w-16 h-16 rounded-full bg-primary-600 text-white flex items-center justify-center hover:bg-primary-700 transition-colors"
                    aria-label="Start recording"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                    </svg>
                  </button>
                ) : (
                  <>
                    <button
                      onClick={startRecording}
                      className="px-4 py-2 border border-primary-600 text-primary-600 rounded-md hover:bg-primary-50 transition-colors"
                    >
                      Record Again
                    </button>
                    
                    <button
                      onClick={handleUpload}
                      disabled={isUploading}
                      className={`px-4 py-2 rounded-md text-white ${
                        isUploading ? 'bg-primary-400 cursor-not-allowed' : 'bg-primary-600 hover:bg-primary-700'
                      } transition-colors`}
                    >
                      {isUploading ? 'Uploading...' : 'Save Recording'}
                    </button>
                  </>
                )}
              </>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default VoiceCapture;
