var x = 0;
var y = 1;
var str333 = "This is a string with \"embedded\" quotes.";
var st = "pisa";

function addInput() {
	if (x < 15) {
    var str = '<div class="row justify-content-center"><div class="mb-3 col-12"><label for="exampleInputEmail1" list="character_one" class="form-label">Symptom '+ (y + 1) +'</label><input class="form-control form-control-lg" type="text" placeholder="Write down your symptom" aria-label="Пример .form-control-lg" data-bs-theme="light" name="field'+ (y+1) +'"autocomplete="off"><datalist id="character_one">'+ st + '<option value="{{ row[0] }}"></option></div></div><div id="input' + (x + 1) + '"></div>';
    document.getElementById('input' + x).innerHTML = str;
    x++;
    y++;
  } else
  {
    document.getElementById("addbutton").classList.add('d-none');
  }
}