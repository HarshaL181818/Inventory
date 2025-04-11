const { spawn } = require('child_process');

function analyzeJD(title, description) {
  return new Promise((resolve, reject) => {
    const py = spawn('python', ['demo/parse_jd.py']); // your script

    let output = '';
    let error = '';

    py.stdout.on('data', data => output += data.toString());
    py.stderr.on('data', data => error += data.toString());

    py.stdin.write(JSON.stringify({ title, description }));
    py.stdin.end();

    py.on('close', code => {
      if (code !== 0 || error) return reject(error || 'Process failed');
      try {
        const parsed = JSON.parse(output.split('###JSON_START###')[1]);
        resolve(parsed);
      } catch (err) {
        reject("Failed to parse JSON from Python");
      }
    });
  });
}

module.exports = { analyzeJD };
