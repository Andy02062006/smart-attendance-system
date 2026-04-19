let mediaRecorder;
let recordedChunks = [];

function toggleRecording() {
    const btn = document.getElementById('recordBtn');
    const status = document.getElementById('recordingStatus');

    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
        startRecording(btn, status);
    } else {
        stopRecording(btn, status);
    }
}

async function startRecording(btn, status) {
    try {
        const stream = await navigator.mediaDevices.getDisplayMedia({ video: true, audio: true });
        mediaRecorder = new MediaRecorder(stream);
        recordedChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) recordedChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: 'video/webm' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `lecture_${new Date().getTime()}.webm`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        };

        mediaRecorder.start();
        btn.innerText = 'Stop Recording';
        btn.classList.add('btn-primary');
        btn.classList.remove('btn-outline');
        status.style.display = 'flex';
        console.log('Recording started');
    } catch (err) {
        console.error('Error starting recording:', err);
        alert('Could not start screen recording. Please grant permissions.');
    }
}

function stopRecording(btn, status) {
    mediaRecorder.stop();
    btn.innerText = 'Start Lecture Recording';
    btn.classList.add('btn-outline');
    btn.classList.remove('btn-primary');
    status.style.display = 'none';
    
    // Stop all tracks to release the stream
    mediaRecorder.stream.getTracks().forEach(track => track.stop());
    console.log('Recording stopped');
}
