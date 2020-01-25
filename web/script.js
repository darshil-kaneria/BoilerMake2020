
function getInput(){
  let user_song = document.getElementById('textbox').value;
  alert("output: " + user_song);
}

//for playing audio
var log = document.getElementById('log');
var btn = document.getElementById('btn');
function report(s) { return function() { log.innerHTML = s; }; }

JZZ.synth.Tiny.register('Web Audio');
var out = JZZ().or(report('Cannot start MIDI engine!')).openMidiOut().or(report('Cannot open MIDI Out!'));
var player;
var playing = false;

function clear() {
  if (player) player.stop();
  playing = false;
  btn.innerHTML = 'Play';
  btn.disabled = true;
}

function load(data, name) {
  try {
    player = JZZ.MIDI.SMF(data).player();
    player.connect(out);
    player.onEnd = function() {
      playing = false;
      btn.innerHTML = 'Play';
    }
    playing = false;
    player.play();
    log.innerHTML = name;
    btn.innerHTML = 'Stop';
    btn.disabled = false;
  }
  catch (e) {
    log.innerHTML = e;
  }
}

function playStop() {
  if (playing) {
    player.stop();
    playing = false;
    btn.innerHTML = 'Play';
  }
  else {
    player.play();
    playing = true;
    btn.innerHTML = 'Stop';
  }
}

function fromFile() {
  clear();
  var reader = new FileReader();
  var f = document.getElementById('file').files[0];
  reader.onload = function(e) {
    var data = '';
    var bytes = new Uint8Array(e.target.result);
    for (var i = 0; i < bytes.length; i++) {
      data += String.fromCharCode(bytes[i]);
    }
    load(data, f.name);
  };
  reader.readAsArrayBuffer(f);
}
