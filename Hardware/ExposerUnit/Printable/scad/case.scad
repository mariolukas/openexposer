include <config.scad>;

translate([0,0,30]) rotate([0,180,0]) top_case();
rotate([0,180,0])  bottom_case();

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
   	base_form(case_width,case_length,wall_thickness);

  difference(){
	translate([0,0,case_height/5-wall_thickness]) 
       base_form(case_width-wall_thickness*2,case_length-wall_thickness*2,case_height/5);
	
    translate([0,0,case_height/5+0.1-wall_thickness]) 
       base_form(case_width-wall_thickness*4,case_length-wall_thickness*4,case_height/5);
  }

  } 
 	// Mirror mount slor
	translate([(case_length/2)-13,0,-wall_thickness]) cube([3,case_width,case_height],true);
    translate([(case_length/2)-25,0,case_height/3-wall_thickness-0.65]) 
        cube([50,case_width+60,case_height/3+1],true);
}

}


module bottom_case(){
  difference(){
    
    // Base Form of Bottom Case
   	base_form(case_width,case_length,case_height);
   	translate([0,0,-wall_thickness]) 
	  base_form(case_width-wall_thickness*2,case_length-wall_thickness*2,case_height);
	
     translate([10,-case_width/2-3,0]){ 
		 rotate([0,90,90]) cylinder(5,28/2,28/2,true);
	    translate([11.8,0,11.8]) rotate([0,90,90]) cylinder(5,3/2,3/2,true);
	    translate([11.8,0,-11.8]) rotate([0,90,90]) cylinder(5,3/2,3/2,true);
		translate([-11.8,0,11.8]) rotate([0,90,90]) cylinder(5,3/2,3/2,true);
   		translate([-11.8,0,-11.8]) rotate([0,90,90]) cylinder(5,3/2,3/2,true);
    }
    // Polygon Mirror Holes
	translate([-20,0,case_height/2-wall_thickness/2])
      rotate([0,0,90])  polygon_mirror_screw_holes();

	// Polygon Mirror Bottom Hole
	translate([-30,0,case_height/2]) 
      rotate([0,0,90]) cube([screw_distance_y/1.2,screw_distance_x/1.6,wall_thickness+2],true);

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

	// Mirror mount slor
	translate([(case_length/2)-5,0,-wall_thickness]) cube([4,case_width*2,case_height],true);
	
	// laser mount hole
    translate([screw_distance_y/4+2,-screw_distance_x/2-16,case_height/2-wall_thickness/2]) 
      cylinder(wall_thickness+2,1.6,1.6,true);

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
