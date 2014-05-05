$fn = 50;
screw_distance_x = 60;
screw_distance_y = 40;
wall_thickness = 2.5;

case_width = screw_distance_x*2;
case_length = screw_distance_y*2.25+15;
case_height = 32;



bearing_diameter = 16;
bearing_length = 28;

//rotate([0,180,0]) exposer_case_bottom();
//rotate([0,180,0]) translate([0,0,-18])
//  exposer_case_top();
//translate([-12,-45,-case_height+23]) rotate([0,0,60])laser_mount();

translate([0,20,0]) laser_mount();
//laser_mount_light();

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

module laser_mount_light(){
	translate([0,0,-5]){
	    cube([25,16,3],true);
	    translate([25/2,0,3.2]) cube([3,16,10],true);
     	translate([-25/2,0,3]) cube([3,16,10],true);
    }
	
	translate([0,0,6.5]) rotate([0,90,0]) cylinder(30,6.2,6.2,true);

}

/*
mirror([1,0,0]) translate([10,0,0])
	rotate([0,90,0]) 
   mirror_mount();
*/

/*
mirror([0,0,0]) translate([10,0,0])
	rotate([0,90,0]) 
   mirror_mount_with_sensor();
*/

module mirror_mount_with_sensor(){


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

module base_form(width,length,height){
    
   translate([-length/2,-width/2,0]) minkowski(){
	cube([length,width,height],true);
    translate([length/2,width/2,0]) cylinder(1,5,5,true);
   }
   
}


module exposer_case_top(){
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

   translate([52,-40,-1]) rotate([0,0,90]) wall_stabilizer();
	translate([52,0,-1]) rotate([0,0,90]) wall_stabilizer();
	translate([52,40,-1]) rotate([0,0,90]) wall_stabilizer();
}

module wall_stabilizer(){
	hull(){
	  translate([0,0,5])cube([2,2,case_height/5],true);
	  translate([0,3,2])cube([2,3,1],true);
    }
}





module exposer_case_bottom(){
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
	/*
	#translate([screw_distance_y/4,-10,case_height/2]){
	  cylinder(wall_thickness*3,1.6,1.6,true);
      translate([20,0,0])cylinder(wall_thickness*3,1.6,1.6,true);
    }
	*/

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
