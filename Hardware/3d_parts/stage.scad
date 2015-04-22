$fn = 60;
stage();
module stage(){
 difference(){ 
  union(){
	cylinder(40,20,20,true);
	translate([0,0,-10]) cylinder(20,35,35,true);
   }
	cylinder(43,4.3,4.3,true);
	translate([0,0,-17]) cylinder(6,15.4/2,15.4/2,true, $fn=6);
 }

}