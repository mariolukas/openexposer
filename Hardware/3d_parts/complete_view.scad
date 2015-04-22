include <exposer_box.scad>;
include <NEMAMount.scad>;
include <servo.scad>;
include <hardware.scad>;

//rotate([90,0,90]) bottom_back_connector();
//rotate([90,0,90]) bottom_front_connector();
//rotate([0,180,0]) top_motor_mount();
//rotate([90,270,0]) mirror([0,1,0]) rod_corner_mount();
//rotate([0,180,0]) vat_mount();
//rotate([0,180,0]) bottom_motor_mount();
//stage_carrier();
//rotate([90,0,0]) vat_mount_carrier();
//rotate([90,0,0]) front_rod_vat_mount();
//complete_3d();
//rotate([0,90,0]) back_motor_mount();
//rotate([0,270,0]) back_motor_nut_mount();
//vat_mount();
//translate([-115,-38,45]) rotate([0,180,-90])  vat_clamp();
//translate([-188.5,34,40]) rotate([180,0,139])  vat_clamp();
//complete_3d();
//translate([-95,36.5,43]) rotate([-90,-90,0]) servoSG90();
translate([-111,65,50]) rotate([0,0,0]) servo_arm();
//translate([-210,55,30]) rotate([-90,0,0]) vat_mount_carrier(true);
//vat_mount();

module servo_arm(){
//translate([-6.2,-3,-1.5]) rotate([0,0,60]) cube([5,2.85,3]);

 translate([0,0,-3])
  hull(){
	translate([-8,0,0])  cylinder(3,5,5,true);
     translate([23,0,0])  cylinder(3,5,5,true); 
	
  }
  
difference(){ 
 hull(){
	translate([9,0,0])  cylinder(3,5,5,true);
     translate([23,0,0]) cylinder(3,5,5,true); 
	
  }



 translate([8,0,1.5]) hull(){
	translate([0,0,0])  cylinder(3,2.3,2.3,true);
     translate([15,0,0]) cylinder(3,3.4,3.4,true); 
	
  }
    translate([23,0,0.7]) cylinder(3,3,3,true); 
 translate([23,0,0.7]) cylinder(10,0.5,0.5,true); 
//translate([-1,-2,0]) cylinder(5,4,4,true);	
// translate([-1,-2,0]) cylinder(5,4,4,true);	
//  translate([-14,0,-3]) rotate([0,0,-30]) cube([19,5,5]);
}
}

module vat_clamp(){
	difference(){
	union(){
		translate([0,0,-0.5]) cylinder(6,6,6,true);
		translate([-5,0,-0.5]) cube([12,10,6],true);
     }
	translate([-55.5,0,-5]) cylinder(25,95/2,95/2,true,$fn=100);
	translate([-52,0,-8]) cylinder(15,96/2,96/2,true,$fn=100);
	translate([1,0,-5]) cylinder(20,1.7,1.7,true);
	}
}

module complete_3d(){
//translate([70,-75,-20]) rod_corner_mount();
translate([65,70,0]) mirror([90,0,0]) rod_corner_mount();
translate([65,-70,0]) rotate([0,0,180]) rod_corner_mount();

translate([-245,70,0]) rod_corner_mount();
translate([-245,-70,0]) rotate([0,0,180]) mirror([90,0,0]) rod_corner_mount();


translate([-205,78,20])  front_rod_vat_mount();
translate([-205,-78,20])  front_rod_vat_mount();

translate([-65,78,210]) top_connector();
translate([-65,-78,210]) top_connector();

translate([37,-78,20]) rotate([0,-25,0]) bottom_back_connector();
translate([37,78,20])  rotate([0,-25,0]) bottom_back_connector();


translate([-80,78,20]) 	bottom_front_connector();
translate([-80,-78,20]) bottom_front_connector();

translate([-68,0,216]) top_motor_mount();
translate([-112,0,24]) rotate([0,180,0]) bottom_motor_mount();

translate([-104,0,114]) stage_carrier();

translate([-2,0,20]) vat_mount();

translate([-210,-58,30]) vat_mount_carrier();
translate([-210,55,30]) vat_mount_carrier(true);

translate([58,5,0]) back_motor_mount();

rods_and_motor();
translate([-45,0,-7]) box();


translate([-55,0,-25.5]) back_motor_nut_mount();
}

module back_motor_nut_mount(){

 difference(){
  union(){
	//cube([10,50,5],true);
	translate([-10,21,-4]) cube([10,11,11],true);
	translate([-10,21,0.5]) cube([10,25,3],true);
	//translate([0,25,-2.8]) rotate([0,90,0]) cylinder(10.2,5,5,true);
   }
	translate([-7,21,-3.5]) rotate([0,90,0]) cylinder(4.2,4.8,4.8,true, $fn=6);
	translate([-12,21,-3.5]) rotate([0,90,0]) cylinder(20,3,3,true);
	translate([-10,12,0]) rotate([0,0,0]) cylinder(20,1.6,1.6,true);
	translate([-10,30,0]) rotate([0,0,0]) cylinder(20,1.6,1.6,true);
	
 }
	
}

module vat_mount_carrier(servomount){
 if (servomount){
  difference(){
  union(){
     translate([121.9,1.5,17]) cube([17.5,7,48],true);
     translate([122.8,1.5,-6]) rotate([0,90,90]) cylinder(7,8,8,true);
   }
    // cut out rod 
    translate([120,0,0]) rotate([0,90,90]) cylinder(12,4.3,4.3,true);
    
    // hole for servo
    translate([122.1,0,24.2]) cube([12.5,12,24.3],true);
    // screws
    translate([122.1,0,39]) rotate([0,90,90]) cylinder(12,1.2,1.2,true);
    translate([122.1,0,10]) rotate([0,90,90]) cylinder(12,1.2,1.2,true);
   
    translate([122.1,9,39]) rotate([0,90,90]) cylinder(12,2,2,true);
    translate([122.1,9,10]) rotate([0,90,90]) cylinder(12,2,2,true);
  }	
 }
 difference(){
   union(){
	rotate([0,90,90]) cylinder(10,8,8,true);
	translate([120,0,0]) rotate([0,90,90]) cylinder(10,8,8,true);
	translate([60,0,-10]) cube([125,10,8],true);
  }

	rotate([0,90,90]) cylinder(12,4.3,4.3,true);
	translate([120,0,0]) rotate([0,90,90]) cylinder(12,4.3,4.3,true);
	translate([18,0,0]) cylinder(40,2.3,2.3,true);
	translate([98,0,0]) cylinder(40,2.3,2.3,true);
	translate([58,0,0]) cylinder(40,2.3,2.3,true);

	translate([58,0,-12]) cylinder(4,7.9/2,7.9/2,true);
	translate([18,0,-12]) cylinder(4,7.9/2,7.9/2,true);
	translate([98,0,-12]) cylinder(4,7.9/2,7.9/2,true);
 }
}

module vat_mount(){


   difference(){
    union(){
	translate([-150,0,30]) cylinder(8,105/2,105/2,true,$fn=100);
	translate([-150,-58,30]) cylinder(8,8,8,true);
	//translate([-110,-41,30]) cube([10,35,6],true);
	translate([-150,-51,30]) cube([15,20,8],true);

	translate([-110,42,30]) cube([10,35,8],true);
	
      translate([-110,55,30]) cylinder(8,8,8,true);
	
	 translate([-190,42,30]) cube([10,35,8],true);
	 translate([-190,55,30]) cylinder(8,8,8,true);

	 translate([-190,36,30]) cylinder(8,5,5,true);
	 translate([-115,-38,30]) cylinder(8,5,5,true);
      translate([-110,65,28]) rotate([0,90,90]) cylinder(8,2,2,true);
      //#translate([-113,61,26])  cube([5,8,5]);
    }

	  translate([-115,-38,30]) cylinder(20,1.7,1.7,true);
 	  translate([-189.5,35,30]) cylinder(20,1.7,1.7,true);
	
	//#translate([-150,0,37]) cylinder(15,92/2,92/2,true);
	//translate([-150,0,40]) cylinder(15,100/2,100/2,true);
	translate([-150,0,30]) cylinder(15,89.5/2,89.5/2,true,$fn=100);
	translate([-150,0,36]) cylinder(15,95/2,95/2,true,$fn=100);
	
	//#translate([18,0,30]) cylinder(20,1.6,1.6,true);
		
	translate([-150,-62,36.5]) cube([2.5,10,10],true);
	translate([-150,-58,37.8]) cylinder(10,6.2,6.2,true);
	translate([-150,-58,0]) cylinder(120,2.5,2.5,true);

	
	translate([-190,62,36.5]) cube([2.5,10,10],true);
	translate([-190,55,37.8]) cylinder(10,6.2,6.2,true);
	translate([-190,55,0]) cylinder(120,2.5,2.5,true);


     translate([-110,62,36.5]) cube([2.5,10,10],true);
	translate([-110,55,37.8]) cylinder(10,6.2,6.2,true);	
	translate([-110,55,0]) cylinder(120,2.5,2.5,true);
	
  }

 // #translate([-110,-41,30]) cube([10,35,6],true);

}

module box(){
	translate([0,0,18]) rotate([0,0,180]) top_case();
	rotate([0,180,0])  bottom_case();
	translate([22,0,-case_height/2+wall_thickness]) rotate([0,0,180]) polygon_mirror();
	#translate([31,46,-23]) rotate([0,90,0]) bearingLM8UU(); 
	#translate([31,-46,-23]) rotate([0,90,0]) bearingLM8UU(); 
	
}

module back_motor_mount(){

difference(){
  union(){
    rotate([0,90,90]) cylinder(10,9,9,true);
    translate([0,32.1,0]) rotate([0,90,90]) cylinder(10,9,9,true);
    translate([7.3,-5,-50]) cube([5,42,55]);
    translate([7.3,30,-22]) cube([5,53,15]);
 }
   translate([6,16,-64]) rotate([0,90,0]){
      translate([-35,0,3.8]) cylinder(14,12,12,true);
	 translate([-35,0,5]) cylinder(40,4,4,true);

	translate([-50.5,15.5,5]) cylinder(40,1.9,1.9,true);
	translate([-50.5,-15.5,5]) cylinder(40,1.9,1.9,true);

	translate([-19.5,15.5,5]) cylinder(60,1.9,1.9,true);
	translate([-19.5,-15.5,5]) cylinder(60,1.9,1.9,true);
  }
    translate([10,73,-15]) rotate([0,90,0]) cylinder(10,4.3,4.3,true);
    translate([0,20,0]) rotate([0,90,90]) cylinder(60,4.3,4.3,true);
    
	translate([0,16,5]) rotate([90,0,90]) cylinder(60,11,11,true);
    		
}
}

module rods_and_motor(){
	#translate([-125,22,265]) rotate([0,180,180]) nema17(); 
	
	//back
	#translate([120,42,-8]) rotate([0,90,180]) nema17(); 
	// bearings
	#translate([-90,-15,100]) rotate([0,0,0]) bearingLM8UU(); 
	#translate([-90, 15,100]) rotate([0,0,0]) bearingLM8UU(); 	

	// bearing rods
	#translate([-90,46,-30]) rotate([0,90,0]) cylinder(300,4,4,true);
	#translate([-90,-46,-30]) rotate([0,90,0]) cylinder(300,4,4,true);

	#translate([-90,78,20]) rotate([0,90,0]) cylinder(300,4,4,true);
	#translate([-90,-78,20]) rotate([0,90,0]) cylinder(300,4,4,true);
	
	// z threaded rod
	#translate([-80,-78,120]) rotate([0,0,0]) cylinder(200,4,4,true);
	#translate([-80,78,120]) rotate([0,0,0]) cylinder(200,4,4,true);

	// z rod
	#translate([-90,-15,120]) rotate([0,0,0]) cylinder(160,4,4,true);
	#translate([-90,15,120]) rotate([0,0,0]) cylinder(160,4,4,true);

     // Motor rod
	#translate([-104,1,120]) rotate([0,0,0]) cylinder(160,2,2,true);

	// trinangle rod
	#translate([-12,-78,125]) rotate([0,-25,0]) cylinder(230,4,4,true);
	#translate([-12,78,125]) rotate([0,-25,0]) cylinder(230,4,4,true);
	
	//translate([-45,0,210]) rotate([0,90,90]) cylinder(180,4,4,true);
	#translate([-90,0,210]) rotate([0,90,90]) cylinder(180,4,4,true);
	#translate([-90,0,30]) rotate([0,90,90]) cylinder(180,4,4,true);
	#translate([-210,0,30]) rotate([0,90,90]) cylinder(180,4,4,true);

	// front rod
	#translate([-237,0,0]) rotate([0,90,90]) cylinder(180,4,4,true);
	#translate([58,0,0]) rotate([0,90,90]) cylinder(180,4,4,true);

	// side rod
	#translate([-90,78,-15]) rotate([0,90,0]) cylinder(320,4,4,true);
	#translate([-90,-78,-15]) rotate([0,90,0]) cylinder(320,4,4,true);

	#translate([-90,21,-29]) rotate([0,90,0]) cylinder(320,2.5,2.5,true);
	// petri mount
	difference(){
	   %translate([-150,0,55]) cylinder(15,95/2,95/2,true);
   	  // translate([-150,0,42]) cylinder(15,92/2,92/2,true);
     }
	//%translate([-150,0,70]) cylinder(150,8/2,8/2,true);
	//translate([-70,-46,-23]) cube([10,10,10],true);
}

module top_connector(){
difference(){  
 union(){	
	translate([-23,0,0]) rotate([0,90,90]) cylinder(15,10,10,true);

	translate([-10,0,0]) cube([30,15,20],true);

	translate([10,0,4]) rotate([0,60,0])  cube([20,15,15],true);
	translate([3,0,0]) rotate([0,90,90]) cylinder(15,10,10,true);
	translate([17,0,8]) rotate([0,90,90]) cylinder(15,10,10,true);
  }
	 translate([-15,0,0]) cylinder(30,4.2,4.2,true);
	 translate([13.3,0,0]) rotate([0,-25,0]) cylinder(50,4.2,4.2,true);
	 translate([-25,0,0]) rotate([0,90,90]) cylinder(30,4.2,4.2,true);
}
}

module bottom_front_connector(){

difference(){
  hull(){
     translate([0,0,25]) rotate([0,90,90]) cylinder(15,10,10,true);
     translate([-5,0,0]) cube([35,15,15],true);
  }

   translate([0,0,20]) cube([13.6,25.4,6.9],true);
   //translate([0,0,33]) cube([25,25,4],true);
   translate([0,0,30]) cylinder(20,4.1,4.1,true);
  translate([-10,0,10])rotate([0,90,90]) cylinder(20,4.2,4.2,true);
   translate([0,0,0]) rotate([0,90,0]) cylinder(60,4.2,4.2,true);
}

}

module bottom_back_connector(){
difference(){ 
 union(){
  hull(){	
	translate([0,0,20]) rotate([0,90,90]) cylinder(15,10,10,true);
	translate([0,0,0]) rotate([0,90,90]) cylinder(15,10,10,true);
   }


	hull(){
		translate([0,0,0]) rotate([0,90,90]) cylinder(15,10,10,true);
		translate([-10,0,4.5]) rotate([0,90,90]) cylinder(15,10,10,true);
     }
 }
	
	 translate([0,0,12]) cube([13.6,25.4,6.9],true);
      //translate([0,0,29]) cube([25,25,4],true);
	translate([10,0,-2]) rotate([0,115,0]) cube([25,25,4],true);
	translate([-20,0,8]) rotate([0,115,0]) cube([25,25,4],true);
	translate([0,0,30]) cylinder(40,4.2,4.2,true);
	rotate([0,115,0]) cylinder(70,4.2,4.2,true);
}
}

module top_motor_mount(){
  difference(){
    union(){
     translate([-36,0,1.5]) cube([44,46,6],true);
     //#translate([23,0,-6]) rotate([0,90,90]) cylinder(46,8,8,true);
	translate([-22,15.5,-6]) rotate([0,90,90]) cylinder(15,8,8,true);
	translate([-22,-15.5,-6]) rotate([0,90,90]) cylinder(15,8,8,true);
		
	translate([-22,15,-15]) cylinder(18,7,7,true);
	translate([-22,-15,-15]) cylinder(18,7,7,true);
     hull(){
	  translate([-28,15,-10]) cube([1,5,20],true);
       translate([-48,15,0]) cube([1,5,4],true);
     }

     hull(){
	  translate([-28,-15,-10]) cube([1,5,20],true);
       translate([-48,-15,0]) cube([1,5,4],true);
     }
    }
	 translate([-22,15,-25]) cylinder(15,4.2,4.2,true);
	 translate([-22,-15,-25]) cylinder(15,4.2,4.2,true);
	 translate([-22,0,-6]) rotate([0,90,90]) cylinder(60,4.2,4.2,true);
     // #translate([-35,0,10]) Simple_NEMA_Mount (NEMA_Size, shaft, pilot, 30, nut_size, nut_height, adjust);
      //motor
   translate([-1.5,0,0]){
      translate([-35,0,-10.2]) cylinder(40,12,12,true);

	 translate([-35,0,5]) cylinder(40,4,4,true);

	translate([-50.5,15.5,5]) cylinder(40,1.9,1.9,true);
	translate([-50.5,-15.5,5]) cylinder(40,1.9,1.9,true);

 }
 }

}


module stage_carrier(){
 difference(){
  union(){
	translate([15,0,0]) cube([8,15,25],true);
	translate([-20,0,-8.5]) rotate([0,90,0]) cube([8,35,75],true);
     translate([14,15,0]) cylinder(25,9.5,9.5,true);
	translate([14,-15,0]) cylinder(25,9.5,9.5,true);
     hull(){	
	   translate([5,15.5,0]) cube([1,4,22],true);
	   translate([-35,15.5,-10]) cube([1,4,1],true);
     }

     hull(){	
	   translate([5,-15.5,0]) cube([1,4,22],true);
	   translate([-35,-15.5,-10]) cube([1,4,1],true);
     }
  	translate([0,1,-3]) cylinder(5,8,8,true);
   }
   hull(){
	translate([-60,0,-8.5]) cylinder(8.8,4.5,4.5,true);
	translate([-40,0,-8.5]) cylinder(8.8,4.5,4.5,true);
   }
  	translate([14,15,0]) cylinder(26,15.2/2,16/2,true);
	translate([14,-15,0]) cylinder(26,15.2/2,16/2,true);
     translate([20,15,0]) cube([10,1.5,28],true); 
	translate([20,-15,0]) cube([10,1.5,28],true); 
     translate([0,1,-10]) cylinder(20,3,3,true);
	
	
	translate([0,1,-3]) cylinder(5.2,4.8,4.8,true, $fn=6);
 }
}

module bottom_motor_mount(){ 
 difference(){

   union(){
	translate([-22,0,-6]) rotate([0,90,90]) cylinder(46,8,8,true);
	translate([-22,15,-15]) cylinder(15,8,8,true);
	translate([-22,-15,-15]) cylinder(15,8,8,true);
   }
	translate([-22,0,-6]) rotate([0,90,90]) cylinder(55,4.2,4.2,true);
   	translate([-22,15,-32]) cylinder(40,4.2,4.2,true);
	translate([-22,-15,-32]) cylinder(40,4.2,4.2,true);
 }
}


module front_rod_vat_mount(){
difference(){
  hull(){
     translate([-5,0,10]) rotate([0,90,90]) cylinder(15,10,10,true);
     translate([-5,0,0]) cube([20,15,15],true);
  }

   //translate([0,0,33]) cube([25,25,4],true);
   translate([-5,0,10])rotate([0,90,90]) cylinder(20,4.1,4.1,true);
   translate([0,0,0]) rotate([0,90,0]) cylinder(60,4.1,4.1,true);
}
}

module rod_corner_mount(){
difference(){
   union(){

 	hull(){
	  translate([0,8,18]) rotate([0,90,0]) cylinder(15,10,10);
	  translate([0,8,-30]) rotate([0,90,0]) cylinder(15,10,10);
     }

     hull(){
	  translate([0,8,-30]) rotate([0,90,0]) cylinder(15,10,10);
	  translate([0,-4,-40]) rotate([0,90,0]) cylinder(15,10,10);
     }
	
	hull(){
	  translate([0,-4,-40]) rotate([0,90,0]) cylinder(15,10,10);
 	  translate([0,-25,-40]) rotate([0,90,0]) cylinder(15,10,10);
     }
   }

 	
   translate([0,-31.5,-53]) difference(){
      translate([8,8,20]) rotate([0,90,0]) cylinder(4,8,8,true);
     translate([8,8,20]) rotate([0,90,0]) cylinder(4,6,6,true);
   }	

   difference(){
      translate([8,8,20]) rotate([0,90,0]) cylinder(4,8,8,true);
     translate([8,8,20]) rotate([0,90,0]) cylinder(4,6,6,true);
   }
   
   translate([20,-24,-30]) rotate([0,90,0]) cylinder(30,4.1,4.1,true);
   translate([10,8,20]) rotate([0,90,0]) cylinder(12,4.1,4.1,true);
   translate([3,10,25]) cube([33,25,10],true);
	//%translate([0,-46,-23]) rotate([0,90,0]) cylinder(30,4,4,true);
   translate([5,8,-15]) rotate([0,90,0]) cylinder(30,4.1,4.1,true);
   translate([8,10,-0.1]) rotate([0,90,90]) cylinder(30,4.1,4.1,true);
}
}
