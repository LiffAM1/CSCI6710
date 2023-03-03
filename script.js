// array of json objects
/*
*/
var classmate_data = [];

function reprocessVampire() {
    var rows = document.getElementById("vampire_table").rows;
    for (var x = 1; x < rows.length; x++) {
        var row = rows[x];

        var student = classmate_data[i]

        var isVampire = isStudentAVampire(student.vampireScore);
        student.isVampire = isVampire;

        row.cells[1].innerHTML = isVampire ? "Vampire" : "Human";
    }
}

function insertStudentToTable(id, name, isVampire) {
    var table = document.getElementById("vampire_table");

    var row = table.insertRow(1);
    row.setAttribute("id", id);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    cell1.innerHTML = name;
    cell2.innerHTML = isVampire ? "Vampire" : "Human";
}

function threshold_based(shadow, garlic, complexion, romanianAccent) {
    var vampireScore = 0;

    shadow ? vampireScore -= 5 : vampireScore += 5;
    garlic ? vampireScore -= 5 : vampireScore += 5;
    // Assume higher value means more pale
    complexion > 5 ? vampireScore += 5 : vampireScore -= 5;
    romanianAccent ? vampireScore += 5 : vampireScore -= 5;

    return vampireScore > 0;
}

function submitUserInput() {
    // name
    var name = document.getElementById("student_name").value;

    // shadow
    var shadow = document.getElementById("has_shadow").checked;

    // garlic
    var garlic = document.getElementById("garlic_checkbox").checked;

    // complexion
    var complexion = document.getElementById("complexion_slider").value;

    // accent
    var romanianAccent = parseInt(document.getElementById("accent_select").value) === 3;

    var processing = parseInt(document.getElementById("mySelect").value);
    var isVampire = false;

    if (processing === 1) {
        isVampire = Math.floor(Math.random()*2) === 1;
    }
    else if (processing === 2) {
        isVampire = threshold_based(shadow, garlic, complexion, romanianAccent)
    }

    var student = {
        id: classmate_data.length,
        name,
        shadow,
        garlic,
        complexion,
        romanianAccent,
        isVampire
    }

    classmate_data.push(student);
    insertStudentToTable(student.id, student.name, student.isVampire);
    updateChart();
}

//Model  of MVC
//TODO: create a function for random guess

google.charts.load('current', {'packages':['corechart']});

google.charts.setOnLoadCallback(drawChart);

// Visualization
var chart;
var data;
var options;
var num_vampire = 0;
var num_human = 0;

function updateChart() {
    var num_vampire = classmate_data.filter((item) => item.isVampire).length;
    var num_human = classmate_data.length - num_vampire;
    drawChart();
    data.removeRow(1);
    data.removeRow(0);
    data.insertRows(0, [['Human', num_human]]);
    data.insertRows(1, [['Vampire', num_vampire]]);
          
    chart.draw(data, options);
}

function drawChart() {

    // Create the data table.
    data = new google.visualization.DataTable();
    data.addColumn('string', 'Element');
    data.addColumn('number', 'Number');
    data.addRows([
        ['Human', num_human],
        ['Vampire', num_vampire]
    ]);

    // Set chart options
    options = {'title':'How many vampires in the class?',
                    'width':400,
                    'height':300};

    // Instantiate and draw our chart, passing in some options.
    chart = new google.visualization.PieChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}