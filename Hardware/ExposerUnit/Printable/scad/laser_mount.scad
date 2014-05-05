include <config.scad>;

laser_mount();

module laser_mount(){
  difference(){ 
   cube([25,18,13],true);
   //translate([0,0,7.5]) cylinder(28,10,10,true);
   translate([0,0,6.5]) rotate([0,90,0]) cylinder(26,6.2,6.2,true);
   cylinder(5,3,3,true);
   cylinder(13.2,1.6,1.6,true);
   translate([0,0,11]) cube([30,20,16],true);
   translate([0,0,16]) rotate([0,90,90]) cylinder(30,1.6,1.6,true);
   translate([0,9,16]) rotate([0,90,90])  cylinder(2,3,3,true,$fn=6);

   translate([7,0,7]) difference(){
    rotate([0,90,0]) cylinder(4,12,12,true);
    rotate([0,90,0]) cylinder(4.1,10,10,true);
   }

   translate([-7,0,7]) difference(){
    rotate([0,90,0]) cylinder(4,12,12,true);
    rotate([0,90,0]) cylinder(4.1,10,10,true);
   }
   	
  }
}