import axios from "axios";
import { useState, useRef } from "react";
const AudioRecorder = () => {
  const mimeType = "audio/webm";

  const [permission, setPermission] = useState(false);
  const mediaRecorder = useRef(null);
  const [recordingStatus, setRecordingStatus] = useState("inactive");
  const [stream, setStream] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [audio, setAudio] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);

  const [responseAudio, setResponseAudio] = useState("");

  const getMicrophonePermission = async () => {
    if ("MediaRecorder" in window) {
      try {
        const streamData = await navigator.mediaDevices.getUserMedia({
          audio: true,
          video: false,
        });
        setPermission(true);
        setStream(streamData);
      } catch (err) {
        alert(err.message);
      }
    } else {
      alert("The MediaRecorder API is not supported in your browser.");
    }
  };

  const startRecording = async () => {
    setRecordingStatus("recording");
    setResponseAudio("");
    setAudio("");
    //create new Media recorder instance using the stream
    const media = new MediaRecorder(stream, { type: mimeType });
    //set the MediaRecorder instance to the mediaRecorder ref
    mediaRecorder.current = media;
    //invokes the start method to start the recording process
    mediaRecorder.current.start();
    let localAudioChunks = [];
    mediaRecorder.current.ondataavailable = (event) => {
      if (typeof event.data === "undefined") return;
      if (event.data.size === 0) return;
      localAudioChunks.push(event.data);
    };
    setAudioChunks(localAudioChunks);
  };

  const callApi = (blob) => {
    blob = blob || audioBlob;
    console.log("Audio blob - ", blob);

    const formData = new FormData();
    formData.append("file", blob, "recording.webm");

    console.log("File prepared, sending...");
    // const url = "http://127.0.0.1:5000/upload";
    const url = "http://3.111.150.170//upload";

    axios
      .post(url, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        responseType: "blob",
      })
      // .then((response) => response.json())
      .then((res) => {
        // console.log("Success:", data);
        setResponseAudio(
          //   URL.createObjectURL(new Blob(res.data, { type: "audio/mp3" }))
          URL.createObjectURL(res.data)
        );
        console.log("Audio received - ", responseAudio);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const stopRecording = () => {
    setRecordingStatus("inactive");
    //stops the recording instance
    mediaRecorder.current.stop();
    mediaRecorder.current.onstop = () => {
      //creates a blob file from the audiochunks data
      const audioBlob = new Blob(audioChunks, { type: mimeType });
      //creates a playable URL from the blob file.
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudio(audioUrl);
      setAudioChunks([]);

      setAudioBlob(audioBlob);

      callApi(audioBlob);
    };
  };

  return (
    <div>
      <h2>Audio Recorder</h2>
      <main>
        <div className="audio-controls">
          {!permission ? (
            <button onClick={getMicrophonePermission} type="button">
              Get Microphone
            </button>
          ) : null}
          {permission && recordingStatus === "inactive" ? (
            <button onClick={startRecording} type="button">
              Start Recording
            </button>
          ) : null}
          {recordingStatus === "recording" ? (
            <button onClick={stopRecording} type="button">
              Stop Recording
            </button>
          ) : null}

          {audio && !responseAudio ? (
            <div className="audio-container">
              <audio src={audio} controls></audio>
              <a onClick={() => callApi()}>Download Recording</a>
            </div>
          ) : null}

          {responseAudio ? (
            <div className="audio-container">
              <audio src={responseAudio} controls></audio>
            </div>
          ) : null}
        </div>
      </main>
    </div>
  );
};
export default AudioRecorder;
