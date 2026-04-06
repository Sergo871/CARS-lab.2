// ============================================
//  Lab 3 – JavaScript: Procesare formular
//  Caracteristici Automobile
// ============================================

// Culori disponibile cu coduri hex
const CULORI = {
  "negru":   { hex: "#1a1a1a", label: "Negru" },
  "alb":     { hex: "#f5f5f5", label: "Alb" },
  "rosu":    { hex: "#cc2200", label: "Roșu" },
  "albastru":{ hex: "#1a4a99", label: "Albastru" },
  "gri":     { hex: "#888888", label: "Gri" },
  "portocaliu":{ hex: "#e05a00", label: "Portocaliu" }
};

// Validare câmp numeric
function valideazaNumar(id, min, max) {
  var input = document.getElementById(id);
  var eroare = document.getElementById("err_" + id);
  var val = parseFloat(input.value);

  if (input.value === "" || isNaN(val)) {
    input.classList.add("invalid");
    eroare.textContent = "Câmpul este obligatoriu!";
    eroare.style.display = "block";
    return false;
  }
  if (val < min || val > max) {
    input.classList.add("invalid");
    eroare.textContent = "Valoare acceptată: " + min + " – " + max;
    eroare.style.display = "block";
    return false;
  }

  input.classList.remove("invalid");
  eroare.style.display = "none";
  return true;
}

// Curata erorile la input
function curatareEroare(id) {
  var input = document.getElementById(id);
  var eroare = document.getElementById("err_" + id);
  input.classList.remove("invalid");
  eroare.style.display = "none";
}

// Clasificare viteza maxima
function clasificareViteza(viteza) {
  if (viteza < 150) return { text: "Oraș", cls: "badge-green" };
  if (viteza < 200) return { text: "Sport", cls: "badge-yellow" };
  if (viteza < 250) return { text: "High Performance", cls: "badge-gold" };
  return { text: "Supercar", cls: "badge-red" };
}

// Clasificare consum
function clasificareConsum(consum) {
  if (consum <= 5)  return { text: "Eco", cls: "badge-green" };
  if (consum <= 9)  return { text: "Normal", cls: "badge-yellow" };
  if (consum <= 14) return { text: "Sportiv", cls: "badge-gold" };
  return { text: "Extrem", cls: "badge-red" };
}

// Clasificare putere
function clasificarePutere(cp) {
  if (cp < 100)  return { text: "Economic", cls: "badge-green" };
  if (cp < 250)  return { text: "Standard", cls: "badge-yellow" };
  if (cp < 450)  return { text: "Sport", cls: "badge-gold" };
  return { text: "Supercar", cls: "badge-red" };
}

// Raport putere/greutate
function raportPG(cp, kg) {
  return (cp / kg * 1000).toFixed(2);
}

// Generare analiza text
function genereazaAnaliza(date) {
  var marca = date.marca;
  var model = date.model || "modelul ales";
  var viteza = date.viteza;
  var cp = date.cp;
  var greutate = date.greutate;
  var consum = date.consum;
  var culoare = CULORI[date.culoare].label;
  var pg = raportPG(cp, greutate);

  var analiza = "";

  // Intro
  analiza += "<strong>" + marca + " " + model + "</strong> în <span class='culoare-preview' style='background:" + CULORI[date.culoare].hex + "'></span><strong>" + culoare + "</strong> — o alegere ";

  if (cp >= 450) analiza += "spectaculoasă pentru pasionații de performanță extremă.";
  else if (cp >= 250) analiza += "excelentă pentru cei care caută echilibrul dintre lux și dinamism.";
  else analiza += "inteligentă pentru uz cotidian și eficiență.";

  analiza += "<br><br>";

  // Viteza
  analiza += "Cu o viteză maximă de <strong>" + viteza + " km/h</strong>, ";
  if (viteza >= 250) analiza += "această mașină intră în categoria supercarurilor — puțini o pot egaliza pe circuit. ";
  else if (viteza >= 200) analiza += "mașina oferă performanțe de înaltă clasă, potrivite pentru circuit și autostradă. ";
  else analiza += "mașina este ideală pentru condus urban și interurban. ";

  // Putere și greutate
  analiza += "Cei <strong>" + cp + " CP</strong> la un raport putere/greutate de <strong>" + pg + " CP/tonă</strong> ";
  if (pg > 400) analiza += "plasează această mașină printre cele mai agile din categorie. ";
  else if (pg > 200) analiza += "oferă o accelerație plăcută și răspuns prompt al motorului. ";
  else analiza += "asigură un condus liniștit și controlat. ";

  analiza += "<br><br>";

  // Consum
  analiza += "Consumul de <strong>" + consum + "L/100km</strong> este ";
  if (consum <= 5) analiza += "remarcabil de eficient — ideal pentru cei preocupați de mediu și costuri reduse.";
  else if (consum <= 9) analiza += "rezonabil pentru categoria sa, un compromis bun între performanță și economie.";
  else if (consum <= 14) analiza += "specific unui automobil sportiv — performanța are un preț la pompă.";
  else analiza += "ridicat, caracteristic unui motor de înaltă performanță care prioritizează puterea.";

  return analiza;
}

// FUNCTIE PRINCIPALA: procesare formular
function proceseazaFormular() {
  // Validare toate câmpurile
  var ok = true;
  ok = valideazaNumar("viteza", 50, 500) && ok;
  ok = valideazaNumar("cp", 50, 2000) && ok;
  ok = valideazaNumar("greutate", 500, 5000) && ok;
  ok = valideazaNumar("consum", 1, 50) && ok;

  // Validare marca
  var marca = document.getElementById("marca").value;
  var errMarca = document.getElementById("err_marca");
  if (!marca) {
    document.getElementById("marca").classList.add("invalid");
    errMarca.textContent = "Selectați marca!";
    errMarca.style.display = "block";
    ok = false;
  } else {
    document.getElementById("marca").classList.remove("invalid");
    errMarca.style.display = "none";
  }

  // Validare culoare
  var culoare = document.querySelector('input[name="culoare"]:checked');
  var errCuloare = document.getElementById("err_culoare");
  if (!culoare) {
    errCuloare.textContent = "Selectați culoarea!";
    errCuloare.style.display = "block";
    ok = false;
  } else {
    errCuloare.style.display = "none";
  }

  if (!ok) return;

  // Colectare date
  var date = {
    marca:    marca,
    model:    document.getElementById("model").value,
    viteza:   parseFloat(document.getElementById("viteza").value),
    cp:       parseFloat(document.getElementById("cp").value),
    greutate: parseFloat(document.getElementById("greutate").value),
    consum:   parseFloat(document.getElementById("consum").value),
    culoare:  culoare.value
  };

  // Generare rezultat
  var pg = raportPG(date.cp, date.greutate);
  var clViteza  = clasificareViteza(date.viteza);
  var clConsum  = clasificareConsum(date.consum);
  var clPutere  = clasificarePutere(date.cp);
  var analiza   = genereazaAnaliza(date);

  // Populare UI
  document.getElementById("rez_titlu").textContent = date.marca + (date.model ? " " + date.model : "");

  document.getElementById("rez_viteza").textContent  = date.viteza + " km/h";
  document.getElementById("rez_cp").textContent      = date.cp + " CP";
  document.getElementById("rez_greutate").textContent = date.greutate + " kg";
  document.getElementById("rez_consum").textContent  = date.consum + " L/100";
  document.getElementById("rez_pg").textContent      = pg + " CP/t";
  document.getElementById("rez_culoare_dot").style.background = CULORI[date.culoare].hex;
  document.getElementById("rez_culoare_text").textContent     = CULORI[date.culoare].label;

  // Badge-uri
  document.getElementById("badge_viteza").textContent  = clViteza.text;
  document.getElementById("badge_viteza").className    = "badge " + clViteza.cls;
  document.getElementById("badge_consum").textContent  = clConsum.text;
  document.getElementById("badge_consum").className    = "badge " + clConsum.cls;
  document.getElementById("badge_putere").textContent  = clPutere.text;
  document.getElementById("badge_putere").className    = "badge " + clPutere.cls;

  // Analiza
  document.getElementById("rez_analiza").innerHTML = analiza;

  // Afisare
  var rezultatDiv = document.getElementById("rezultat");
  rezultatDiv.style.display = "block";
  rezultatDiv.scrollIntoView({ behavior: "smooth", block: "start" });
}

// Reset formular
function resetFormular() {
  document.getElementById("formAuto").reset();
  document.getElementById("rezultat").style.display = "none";

  // Curata toate erorile
  var inputs = document.querySelectorAll("input, select");
  inputs.forEach(function(el) { el.classList.remove("invalid"); });
  var erori = document.querySelectorAll(".error-msg");
  erori.forEach(function(el) { el.style.display = "none"; });
}
