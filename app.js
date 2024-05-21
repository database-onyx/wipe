const express = require('express');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const path = require('path');
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
let pythonProcess = null;
let scriptCanceled = false; 
// Serve static files from the "assets" directory
// app.use('/assets', express.static(path.join(__dirname, 'assets')));

// Serve the HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});




app.post('/start-python', (req, res) => {
    if (!pythonProcess) {
        // Start the first Python script
        pythonProcess = spawn('python', ['eraser.py']);
        
        pythonProcess.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });

        pythonProcess.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        pythonProcess.on('close', (code) => {
            console.log(`Python process exited with code ${code}`);            

            // // Start the second Python script
            // const secondPythonProcess = spawn('python', ['message.py']);
            
            // secondPythonProcess.stdout.on('data', (data) => {
            //     console.log(`stdout (second script): ${data}`);
            // });

            // secondPythonProcess.stderr.on('data', (data) => {
            //     console.error(`stderr (second script): ${data}`);
            // });

            // secondPythonProcess.on('close', (code) => {
            //     console.log(`Second Python process exited with code ${code}`);
            // });
        });
        pythonProcess = null;

        res.send('Python script started');
    } else {
        res.send('Python script is already running');
    }
});


// Endpoint to stop the Python script
app.post('/stop-python', (req, res) => {
    if (pythonProcess) {
        pythonProcess.kill();
        pythonProcess = null;
        res.send('Python script stopped');
    } else {
        res.send('No Python script is running');
    }
});

app.listen(4000, () => {
    console.log('Server is running on http://localhost:4000');
});
