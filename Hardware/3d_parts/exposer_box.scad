$fn = 50;
screw_distance_x = 60;
screw_distance_y = 40;
wall_thickness = 2.5;

case_width = 120;
case_length = 115;
case_height = 32;

bearing_diameter = 16;
bearing_length = 28;

fan_diameter = 28;

//rotate([0,180,0]) bottom_case();

//translate([-10,-45,-5]) rotate([0,90,-135])  laser();

//rotate([0,180,0]) top_case();

module base_form(width,length,height){
    
   translate([-length/2,-width/2,0]) minkowski(){
	cube([length,width,height],true);
    translate([length/2,width/2,0]) cylinder(1,5,5,true);
   }
   
}


module top_case(){
difference(){
 union(){
    // Base Form of Bottom Case
   	base_form(case_width,case_length,wall_thickness-1.5);

	translate([0,0,-wall_thickness-1]) 
       base_form(case_width-wall_thickness*2-1.5,case_length-wall_thickness*2-1.5,wall_thickness+4);


  } 
 	// Mirror mount slor
	translate([(case_length/2)-8,0,-wall_thickness]) cube([4,case_width,case_height],true);
	translate([0,0,-wall_thickness-2]) 
       base_form(case_width-wall_thickness*2-5,case_length-wall_thickness*2-5,wall_thickness+4);
}

}


module mirror_mount(){
   difference(){
	cube([10,5,10]);
	translate([0,-0.2,0]) rotate([0,45,0]) cube([12,5.5,10]);
   }
}

module bottom_case(){
  
  translate([case_length/2,case_width/2+3,4]) rotate([0,0,180]) mirror_mount();
  translate([case_length/2,-case_width/2+2,4]) rotate([0,0,180]) mirror_mount();		
	//# translate([case_length/2-10.5,-case_width/2,8])  
	//	translate([0,-0.2,0]) rotate([0,45,0]) cube([10,122,5]);
		
  difference(){
    
    // Base Form of Bottom Case
   	base_form(case_width,case_length,case_height);
   	translate([0,0,-wall_thickness]) 
	  base_form(case_width-wall_thickness*2,case_length-wall_thickness*2,case_height);
	

	translate([10,-case_width/2-wall_thickness-1,0]) rotate([0,90,90]) fan_cutout();

    // Polygon Mirror Holes
	translate([-20,0,case_height/2-wall_thickness/2])
      rotate([0,0,90])  polygon_mirror_screw_holes();
	
	// Polygon Mirror Bottom Hole
	translate([-25,0,case_height/2]) 
      rotate([0,0,90]) cube([screw_distance_y/1.2,screw_distance_x/1,wall_thickness+2],true);

     // Front Bearing mount
     translate([case_length/2-bearing_length/2,screw_distance_x/2+16,case_height/2-wall_thickness/2]) 
       rotate([0,0,90]) bearing_hole();
     translate([case_length/2-bearing_length/2,-screw_distance_x+14,case_height/2-wall_thickness/2]) 
    	   rotate([0,0,90]) bearing_hole();

     // Back Bearing mount
     translate([-case_length/2+bearing_length/2,-screw_distance_x+14,case_height/2-wall_thickness/2]) 
		rotate([0,0,90]) bearing_hole();
     translate([-case_length/2+bearing_length/2,screw_distance_x/2+16,case_height/2-wall_thickness/2]) 
       rotate([0,0,90]) bearing_hole();

	
	// laser mount hole
    translate([screw_distance_y/4+2,-screw_distance_x/2-16,case_height/2-wall_thickness/2]) 
      cylinder(wall_thickness+2,1.6,1.6,true);
	
     translate([20,12,15]) cylinder(20,1.6,1.6,true);
	translate([20,30,15]) cylinder(20,1.6,1.6,true);	

  }


	
}

module polygon_mirror_screw_holes(){
  translate([-screw_distance_y/2,screw_distance_x/2,0]) cylinder(wall_thickness+4,1.6,1.6,true);  
  translate([-screw_distance_y/2,-screw_distance_x/2,0]) cylinder(wall_thickness+4,1.6,1.6,true);
  translate([screw_distance_y/2,screw_distance_x/2,0]) cylinder(wall_thickness+4,1.6,1.6,true);
  translate([screw_distance_y/2,-screw_distance_x/2,0]) cylinder(wall_thickness+4,1.6,1.6,true);
}

module bearing_hole(){

    hull(){
   	   translate([0,-bearing_length/2+bearing_diameter/4,0]) 
        cylinder(wall_thickness+2,bearing_diameter/4,bearing_diameter/4,true);
    	 translate([0,bearing_length/2-bearing_diameter/4,0]) 
        cylinder(wall_thickness+2,bearing_diameter/4,bearing_diameter/4,true);
    }
    translate([8,bearing_length/3,0]) cylinder(wall_thickness+3,1.6,1.6,true);
    translate([-8,-bearing_length/3,0]) cylinder(wall_thickness+3,1.6,1.6,true);
    translate([8,-bearing_length/3,0]) cylinder(wall_thickness+3,1.6,1.6,true);
    translate([-8,bearing_length/3,0]) cylinder(wall_thickness+3,1.6,1.6,true);
 
}


module laser(){
  translate([0,0,-30]) cylinder(40,1,1,true);
   #translate([0,-40,-30]) rotate([0,-60,90]) cylinder(80,1,1,true);
   #translate([0,-70,-15]) rotate([90,90,90]) cylinder(80,1,1,true);
   cylinder(30,6,6,true);
}

module polygon_mirror(){
	 cube([67.8,47.8,1],true);
    translate([-8,0,0]){
	 translate([0,0,8.5]) cylinder(2,20,20,true,$fn=6);
     translate([0,0,4.5]) cylinder(9,16,16,true);
	 translate([0,0,-4.5]) cylinder(9,4.5,4.5,true);
   }
}

module fan_cutout(){
	cylinder(wall_thickness+2,fan_diameter/2,fan_diameter/2,true);
    rotate([0,0,45]) translate([0,fan_diameter/2+3,0]) cylinder(wall_thickness+2,1.55,1.55,true);
	rotate([0,0,-45]) translate([0,-fan_diameter/2-3,0]) cylinder(wall_thickness+2,1.55,1.55,true);
	rotate([0,0,-45]) translate([0,fan_diameter/2+3,0]) cylinder(wall_thickness+2,1.55,1.55,true);
	rotate([0,0,45]) translate([0,-fan_diameter/2-3,0]) cylinder(wall_thickness+2,1.55,1.55,true);
}
