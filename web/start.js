var express = require('express');
var app = express();
var path = require('path')



app.get('/', dispHTML);
app.get('/name', callName); 
const serveIndex = require('serve-index');
app.use('/dirs', express.static('web'))
app.use('/dirs', serveIndex('web'))


function dispHTML(req, res){

    res.sendFile('D:\\Work\\College\\Spring 2020\\BoilerMake2020\\web\\Main.html');
    

}
  
function callName(req, res) { 
      
    res.sendFile('D:\\Work\\College\\Spring 2020\\BoilerMake2020\\web\\Main.html')
    console.log("Running python script...");
    // Use child_process.spawn method from  
    // child_process module and assign it 
    // to variable spawn 
    var spawn = require("child_process").spawn; 
      
    // Parameters passed in spawn - 
    // 1. type_of_script 
    // 2. list containing Path of the script 
    //    and arguments for the script  
      
    // E.g : http://localhost:3000/name?firstname=Mike&lastname=Will 
    // so, first name = Mike and last name = Will 
    var process = spawn('python',["D:\\Work\\College\\Spring 2020\\BoilerMake2020\\main\\test.py"]); 
  
    // Takes stdout data from script which executed 
    // with arguments and send this data to res object 
    process.stdout.on('data', (data) => { 
        console.log(data)
    } ) 
} 

app.listen(3000, function() { 
    console.log('server running on port 3000'); 
} );