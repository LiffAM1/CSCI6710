var classmate_data = [];
var chart;
var data;
var options;
var num_vampire = 0;
var num_human = 0;
var model;

$( document ).ready(function() {
    update_slider();
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(draw_chart)
});

function reprocess_classmates() {
    var rows = document.getElementById("vampireTable").rows;
    for (var x = 1; x < rows.length; x++) {
        var row = rows[x];

        var student = classmate_data[x-1]

        student.isVampire = determine_vampire_status(student);

        row.cells[1].innerHTML = student.isVampire ? "Vampire" : "Human";
    }
    update_chart();
}

function build_post_data(student) {
    var sample = {}
    sample["shadow"] = student.shadow;
    sample["garlic"] = student.garlic;
    sample["romanianAccent"] = student.romanianAccent;
    sample["easternAccent"] = student.easternAccent;
    sample["complexion"] = ((11-student.complexion)-5);
    return JSON.stringify(sample);
}

// Call the backend to make a prediction against the TF random forest model
function random_forest_predict(student) {
    var isVampire;
    $.ajax ({
        url: "http://localhost:5000/predict",
        type: "POST",
        data: build_post_data(student),
        dataType: "json",
        async: false,
        contentType: "application/json; charset=utf-8",
        success: function(data) {
            isVampire = data === "Vampire";
        },
        error: function(error) {
            alert("Something bad happened with the prediction: " + error.toString());
        }
    });
    return isVampire;
}


function update_slider() {
    var complexions = ['ghostly','porcelain','pale','fair','light','medium','golden','tan','brown','chocolate','deep'];

    // Update the current slider value (each time you drag the slider handle)
    var slider = document.getElementById("complexionSlider");
    var output = document.getElementById("complexionValue");

    output.innerHTML = complexions[slider.value-1];
}

function add_to_table(id, name, isVampire) {
    var table = document.getElementById("vampireTable");

    var row = table.insertRow(1);
    row.setAttribute("id", id);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = name;
    cell2.innerHTML = isVampire ? "Vampire" : "Human";
}

function determine_vampire_status(student) {
    var processing = parseInt(document.getElementById("processingChoice").value);
    var isVampire = false;

    // Random
    if (processing === 1) {
        isVampire = Math.floor(Math.random()*2) === 1;
    }

    // Threshold-based
    else if (processing === 2) {
        isVampire = calculate_with_threshold(
            student.shadow,
            student.garlic,
            student.complexion,
            student.romanianAccent,
            student.easternAccent);
    }

    // Random Forest
    else if (processing == 3) {
        isVampire = random_forest_predict(student);
    }

    return isVampire;
}

function calculate_with_threshold(shadow, garlic, complexion, romanianAccent, easternAccent) {

    var vampireScore = 0;

    shadow ? vampireScore -= 5 : vampireScore += 5;
    garlic ? vampireScore -= 5 : vampireScore += 5;

    // +5 if they're from Romania, neutral if they're from somewhere in eastern Europe, -5 otherwise
    if (romanianAccent) {
        vampireScore += 5;
    } else if (!easternAccent) {
        vampireScore -= 5; 
    }

    vampireScore += ((11-complexion)-5) // Adds points between -5 (darkest) and 5 (lightest)

    console.log(vampireScore);

    return vampireScore > 0;
}

function submit() {
    // name
    var name = document.getElementById("studentName").value;

    // shadow
    var shadow = document.getElementById("yesShadow").checked;

    // garlic
    var garlic = document.getElementById("garlicCheckbox").checked;

    // complexion
    var complexion = document.getElementById("complexionSlider").value;

    var romanianAccent = false;
    var easternAccent = false;
    // accent
    var accent = parseInt(document.getElementById("accentSelect").value)
    switch (accent) {
        case 'ro':
            romanianAccent = true;
            break;
        case 'md':
        case 'rs':
            easternAccent = true;
            break;      
    }

    var student = {
        'id': classmate_data.length,
        'name': name,
        'shadow': shadow,
        'garlic': garlic,
        'complexion': complexion,
        'romanianAccent': romanianAccent,
        'easternAccent': easternAccent,
        'isVampire': false
    }

    student.isVampire = determine_vampire_status(student);

    classmate_data.push(student);
    add_to_table(student.id, student.name, student.isVampire);
    update_chart();
}

// Visualization
function update_chart() {
    var num_vampire = classmate_data.filter((item) => item.isVampire).length;
    var num_human = classmate_data.length - num_vampire;

    draw_chart();

    data.removeRow(1);
    data.removeRow(0);
    data.insertRows(0, [['Human', num_human]]);
    data.insertRows(1, [['Vampire', num_vampire]]);
          
    chart.draw(data, options);
}

function draw_chart() {

    // Create the data table.
    data = new google.visualization.DataTable();
    data.addColumn('string', 'Element');
    data.addColumn('number', 'Number');
    data.addRows([
        ['Human', num_human],
        ['Vampire', num_vampire]
    ]);

    // Set chart options
    options = {'width':400,'height':400};

    // Instantiate and draw our chart, passing in some options.
    chart = new google.visualization.PieChart(document.getElementById('chartDiv'));
    chart.draw(data, options);
}