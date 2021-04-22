// script to get current date - put this value as end date
var d1 = new Date();
var y1= d1.getFullYear()// - 1;//remove - 1 later
var m1 = d1.getMonth()+1;
if(m1<10)
  m1="0"+m1;
var dt1 = d1.getDate();
if(dt1<10)
  dt1 = "0"+dt1;
var d2 = y1+"-"+m1+"-"+dt1;
document.getElementById('end').value=d2;