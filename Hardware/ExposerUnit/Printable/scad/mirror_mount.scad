include <config.scad>;

module mirror_mount_for_sensor(){


   difference(){ 
    union(){
      translate([0,-1,0]) cube([5,23,18],true);
       // translate([-1,-8,0]) cube([3,14,16],true);
       //rotate([0,90,0]) cylinder(5,8,8,true);

    }
    	color([0,0,255]) translate([-7,1,-5]) rotate([45,0,0]) cube([case_width,5.3,8.5]);
    translate([0,6.9,-5]) rotate([0,90,0]) cylinder(9,1.6,1.6,true);
    translate([0,-8,-3]){
       //translate([-5,0,-6.1]) rotate([0,90,0]) cylinder(10,1.6,1.6);
       translate([-5,0,6.1]) rotate([0,90,0]) cylinder(10,1.6,1.6);
    }
    translate([-3,-12.5,-6]) cube([6.8,6.5,6.5]);
     translate([-2.6,-12.5,-9]) cube([2,7.5,18.5]);
  }
    translate([-8,5.5,0]) cube([10,3.3,8]);

}

module mirror_mount(){


   difference(){ 
    union(){
      translate([0,5,0]) cube([4,12,18],true);
       rotate([0,90,0]) cylinder(4,9,9,true);
    }
    	color([0,0,255]) translate([-7,1,-5]) rotate([45,0,0]) cube([case_width,5.3,8.5]);
    translate([0,6.9,-5]) rotate([0,90,0]) cylinder(9,1.6,1.6,true);
  }
    translate([-6,5.5,0]) cube([5,3.3,8]);


}
