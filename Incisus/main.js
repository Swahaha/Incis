let {app, BrowserWindow} = require('electron')

function createWindow () {
    window = new BrowserWindow({width: 800, height: 600})
    window.loadFile('index.html')

    let {PythonShell} = require('python-shell')
    PythonShell.run('hello.py', null, function  (err, results)  {
    if  (err)  throw err;
    console.log('hello.py finished.');
    console.log('results', results);
    });
 }

app.on('ready', createWindow)

app.on('window-all-closed', () => {
      app.quit()
  })

  
