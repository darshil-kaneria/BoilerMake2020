function getInput(){
  let user_song = document.getElementById('textbox').value;
  alert("output: " + user_song);
}

function playsong(){
  MIDIjs.play('EyesOnMePiano.mid')
}
