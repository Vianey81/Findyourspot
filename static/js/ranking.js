// JS to map and change the data in the index.html

    var width, height, projection, path, graticule, svg, tooltip, color, template;
    var rateById = {};
    var DataById = {};
    var newData = [];
    var state_id = 6;
    var avg_results = {};
    var tax, profession, professionptn, age, marital, wl, wp, wc, wm, sdk, census, ntop, chart_height, offsetL, offsetT;
    
    
function getValuesFrm() {
  // Get the values on the Search Form

    tax = $('#tax').val();
    profession = $('#profession').val();
    professionptn = $('#professionpartner').val();
    age = $('#age').val();
    marital = $('#marital').val();
    wl = $('.opcLiving').val();
    wp = $('.opcProfession').val();
    wc = $('.opcCrime').val();
    wm = $('.opcMarital').val();
    ntop = $('#ntop').val();
    if ($('#tax').val()=='1ad') {
          professionptn = 'None';
      }

}

function showDataRank() {
    // Call the route in python "search_states" and reload the table, and save the new Data in newData array
    var url = "";
    // urlbystate = "";

    getValuesFrm();

    url = "/search_states?tax="+tax+"&profession="+profession+"&professionptn="+professionptn+"&age="+age+"&marital="+marital+"&opcLiving="+wl+"&opcMarital="+wm+"&opcCrime="+wc+"&opcProfession="+wp;
    // urlbystate = "/search_counties?state_id="+state_id+"&tax="+tax+"&profession="+profession+"&professionptn="+professionptn+"&age="+age+"&marital="+marital+"&opcLiving="+wl+"&opcMarital="+wm+"&opcCrime="+wc+"&opcProfession="+wp;

    $.get(url, function(results){
            var data = results['data'];
            for (i=0; i< data.length; i++) {
                if (rateById[data[i].id]) {
                    rateById[data[i].id] = data[i].rate;
                }
                DataById[data[i].id]= { "name":data[i].name,
                                        "totalmarital":data[i].totalmarital,
                                        "livingrank":data[i].livingrank,
                                        "professionrank": data[i].professionrank,
                                        "crimerank":data[i].crimerank,
                                        "rate":data[i].rate};  
        }
        });

}

function init() {
  // Initialize map
  setMap();
  sequenceMap();

}


function setMap() {
      // set the Map
      width = 960; 
      height = 580;  // map width and height, matches 


      tooltip = d3.select("#mapform").append("div").attr("class", "tooltip hidden");
      offsetL = document.getElementById('mapform').offsetLeft+20;
      offsetT = document.getElementById('mapform').offsetTop+10;
                
      projection = d3.geo.albersUsa()   // define our projection with parameters
        .scale(1200)
        .precision(.1);


      path = d3.geo.path()  // create path generator function
          .projection(projection);  // add our define projection to it

      svg = d3.select("#mapform").append("svg")
                .attr("width", width)
                .attr("height", height);

      g = svg.append("g")
                .call(d3.behavior.zoom()
                .scaleExtent([1, 10])
                .on("zoom", zoom));

      var zoom = d3.behavior.zoom()
                .translate(projection.translate())
                .scaleExtent([height, Infinity])
                .scale(projection.scale())
                .on("zoom", function() {
                    projection.translate(d3.event.translate).scale(d3.event.scale)
                    g.selectAll("path.zoomable").attr("d", path);

                    projection.translate(d3.event.translate).scale(d3.event.scale)
                    svg.selectAll(".place").attr("d", path);    

            });
      svg.call(zoom);
      loadData();  // Load the Data

}

function loadData() {


queue()   // queue function loads all external data files 
    .defer(d3.json, "data/us.json")  // load geometries by state
    .defer(d3.tsv, "data/rankresults.tsv")  // and associated data in tsv file
    .await(processData);

}


function loadNewData(){
    // get the newData, wait 100 miliseconds, and then color the map
    async.series([
      showDataRank,
      setTimeout(sequenceMap, 100),
    ]);
    $('#chgChartCP').trigger("click");
    $('#chgChartML').trigger("click");
    $('#nameState').html("TOP States");
    $('#chartsgral').attr("hidden", false);
    $('#chartsbystate').attr("hidden", true);

}

function processData(error,us,matches) {
  // function accepts any errors from the queue function as first argument, then
  // each data object in the order of chained defer() methods above              
  matches.forEach(function (d) { // <-B
      rateById[d.id] = +d.rate;

  });

  drawMap(us);

}

function drawMap(us) {

    svg.selectAll(".states")   // select country objects (which don't exist yet)
      .data(topojson.feature(us, us.objects.states).features)
      .enter().append("path") // prepare data to be appended to paths
      .attr("class", "states") // give them a class for styling and access later
      .attr("id", function(d) { return "code_" + d.id; }, true)
      .attr("d", path)
      .on("mousemove", function(d,i) {
          var mouse = d3.mouse(svg.node()).map( function(d) { return parseInt(d); } );
          tooltip.classed("hidden", false)
                 .attr("style", "left:"+(mouse[0]+offsetL)+"px;top:"+(mouse[1]+offsetT)+"px")
                 .html(DataById[d.id].name)
      })
      .on("mouseout",  function(d,i) {
        tooltip.classed("hidden", true);
      })
      // When a feature is clicked, show the details of it.
      .on('click', function(d){
            showDetails(d.id);
      });
          

}

function move() {

  var t = d3.event.translate;
  var s = d3.event.scale;
  zscale = s;
  var h = height/4;


  t[0] = Math.min(
    (width/height)  * (s - 1),
    Math.max( width * (1 - s), t[0] )
  );

  t[1] = Math.min(
    h * (s - 1) + h * s,
    Math.max(height  * (1 - s) - h * s, t[1])
  );

  zoom.translate(t);
  g.attr("transform", "translate(" + t + ")scale(" + s + ")");

  //adjust the country hover stroke width based on zoom level
  d3.selectAll(".states").style("stroke-width", 1.5 / s);

}

function sequenceMap() {
    // make the transition everytime the data in the map changes
    d3.selectAll('.states').transition()  //select all the countries and prepare for a transition to new values
      .duration(1250)  // give it a smooth time period for the transition
      .style("fill", function (d) {
            return getColor(rateById[d.id]); // <-C
        });

}

function getColor(value) {
  // return a color depending on the value passed
  var color = "white";
 
  if (value >= 1 && value<= 10){
      color = "#edf8e9";
  }
  if (value > 10 && value<= 20){
      color = "#bae4b3";
  }
  if (value > 20 && value<= 30){
      color = "#74c476";
  }
  if (value > 30 && value<= 40){
      color = "#31a354";
  }
  if (value > 40){
      color = "#006d2c";
  }

  return color;  // return that number to the caller
}

function showDetails(id) {
  // Draw the table with the Counties of the selected State, Draw the charts By State
  var d = DataById[id];
  state_id = id;
  getValuesFrm();
  urlbystate = "";

  urlbystate = "/search_counties?state_id="+state_id+"&tax="+tax+"&profession="+profession+"&professionptn="+professionptn+"+&age="+age+"&marital="+marital+"&opcLiving="+wl+"&opcMarital="+wm+"&opcCrime="+wc+"&opcProfession="+wp;

  var table = $('#infotable').DataTable();

  table.ajax.url(urlbystate).load();
  $('#ptable').html("Counties of "+DataById[state_id].name);
  $('#nameState').html(DataById[state_id].name);
  $('#crimebtn').trigger("click");
  $('#maritalbtn').trigger("click");
  $('#agebtn').trigger("click");
  $('#chartsgral').attr("hidden", true);
  $('#chartsbystate').attr("hidden", false);
  
}
    
var app = angular.module('spot', ['nvd3']);

app.controller('MainCtrl', function($scope) {
        

        $scope.optionsbystate = {
            chart: {
                type: 'pieChart',
                height: 250,
                x: function(d){return d.key;},
                y: function(d){return d.y;},
                showLabels: true,
                labelType: "percent",
                donut: true,
                duration: 1500,
            }
        };

        
  

        $scope.datacrime = [];
        $scope.onclickcrime = function(){
           $scope.datacrime = [];
            setTimeout(function(){
                $scope.datacrime = getData("/crime.json?id="+state_id);
                $scope.$apply();
            }, 0);
        };
        
        $scope.datamarital = [];
        $scope.onclickmarital = function(){
           $scope.datamarital = [];
            setTimeout(function(){
                $scope.datamarital = getData("/marital.json?id="+state_id);
                $scope.$apply();
            }, 0);
        };

        $scope.dataage = [];
        $scope.onclickage = function(){
           $scope.dataage = [];
            setTimeout(function(){
                $scope.dataage = getData("/age.json?id="+state_id);
                $scope.$apply();
            }, 0);
        };
        
        function getData(url){
        $.ajax({url: url, async: false, success: function(result){
          data = result['result'];
        }
        });
          return data;
        }

  if ($('#ntop').val()==10) {
      chart_height = 600;
  } else if ($('#ntop').val()==5){
      chart_height = 400;
  } else {
      chart_height = 400;
  }

  $scope.optionsgral = {
            chart: {
                type: 'multiBarHorizontalChart',
                height: chart_height,
                // width: 350,
                x: function(d){return d.label;},
                y: function(d){return d.value;},
                showControls: false,
                showValues: true,
                duration: 500,
                xAxis: {
                    showMaxMin: true
                },
                yAxis: {
                    axisLabel: 'Values',
                    tickFormat: function(d){
                        return d3.format(',.2f')(d);
                    }
                }
            }
        };
        
        $scope.data2 = [];
        $scope.onclickdata2 = function(){
            var urlmarliv = "";
            getValuesFrm();
            urlmarliv = "/chartsgral.json?chart=marliv&tax="+tax+"&profession="+profession+"&professionptn="+professionptn+"&age="+age+"&marital="+marital+"&ntop="+ntop+"&opcLiving="+wl+"&opcMarital="+wm+"&opcCrime="+wc+"&opcProfession="+wp;
            setTimeout(function(){
                
                $scope.data2 = getData(urlmarliv);   
                $scope.$apply();
            }, 0);
            };
            
        $scope.data = [];
        $scope.onclickdata = function(){
          var urlcripro = "";
          getValuesFrm();
          urlcripro = "/chartsgral.json?chart=cripro&tax="+tax+"&profession="+profession+"&professionptn="+professionptn+"&age="+age+"&marital="+marital+"&ntop="+ntop+"&opcLiving="+wl+"&opcMarital="+wm+"&opcCrime="+wc+"&opcProfession="+wp;
        setTimeout(function(){

            $scope.data = getData(urlcripro);   
            $scope.$apply();
        }, 0);
        };
                



});
