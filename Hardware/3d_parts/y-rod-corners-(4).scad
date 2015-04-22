// Open Exposer 3D Printer Extension
// Z motor mount
// GNU GPL v3
// Mario Lukas <info@mariolukas.de>
// http://www.mariolukas.de
// http://www.openexposer.com

corner_out();
// Final part
module corner_out(){
 // Rotate the part for better printing
 translate([0,0,11]) rotate([-90,0,0]) difference(){
  corner_base_out();
  corner_holes_out();
  corner_fancy_out();
 }
}


module corner_back(){
 // Rotate the part for better printing
 translate([0,0,11]) rotate([-90,0,0]) difference(){
  corner_back_base();
  corner_back_holes()
  corner_fancy();
 }
}


module corner_base_out(){	
 translate([-9,-11,0])cube([18,22,103]);
}

module corner_base(){	
 translate([-9,-11,0])cube([18,22,47]);
}

module corner_back_base(){	
 translate([-9,-29,0])cube([18,40,47]);
}



module corner_back_holes(){
 translate([-11,-11,0]){
  // Bottom hole
  translate([0,11,10]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 270, r=4.4, $fn=30);
  // Top hole
  translate([0,11,30]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 270, r=4.4, $fn=30);
  // Middle hole
  //translate([11,0,20]) rotate([0,0,90]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 270, r=4.4, $fn=30);

  // Washer hole
//  translate([11,-3,20]) rotate([0,0,90]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 10, r=11, $fn=30);
  translate([11,-8,5])  cylinder(h = 270, r=4.2, $fn=30);
  // Top smooth rod insert
  // Smooth rod place
  // translate([11,2,45]) rotate([0,90,90]) cylinder(h = 270, r=4.2, $fn=30);
  // Mod for 10mm bar
  translate([11,2,45]) rotate([0,90,90]) cylinder(h = 270, r=4.2, $fn=30); 
  // Ziptie
  translate([-5,10,37]) cube([30,3.5,2]);
  translate([-5,10,37]) rotate([45,0,0]) cube([30,1.42,1.42]);
 }
}

module corner_fancy_out(){
 // Side corner cutouts
  translate([-8,-9,0]) rotate([0,0,-45-180]) translate([-15,0,-1]) cube([30,30,101]);
  translate([8,-9,0]) rotate([0,0,45-180]) translate([-15,0,-1]) cube([30,30,101]);
 // Top corner cutouts
 translate([7,0,101]) rotate([0,45,0]) translate([-15,-15,0]) cube([30,30,30]);
  translate([-7,0,101]) rotate([0,-45,0]) translate([-15,-15,0]) cube([30,30,30]);
  rotate([0,0,90]){
   translate([-9,0,101]) rotate([0,-45,0]) translate([-15,-15,0]) cube([30,30,30]);
  }
}

module corner_holes_out(){
 translate([-11,-11,0]){
  // Bottom hole
  translate([0,11,10]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 270, r=4.4, $fn=30);
  // Top hole
  translate([0,11,30]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 270, r=4.4, $fn=30);
  // Middle hole
  translate([11,0,20]) rotate([0,0,90]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 270, r=4.4, $fn=30);

  translate([11,-20,93]) rotate([0,90,90]) cylinder(h = 270, r=4.2, $fn=30); 
 }
}




module corner_holes(){
 translate([-11,-11,0]){
  // Bottom hole
  translate([0,11,10]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 270, r=4.4, $fn=30);
  // Top hole
  translate([0,11,30]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 270, r=4.4, $fn=30);
  // Middle hole
  translate([11,0,20]) rotate([0,0,90]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 270, r=4.4, $fn=30);

  // Washer hole
  translate([11,-3,20]) rotate([0,0,90]) rotate([0,90,0]) translate([0,0,-5]) cylinder(h = 10, r=11, $fn=30);

  // Top smooth rod insert
  // Smooth rod place
  // translate([11,2,45]) rotate([0,90,90]) cylinder(h = 270, r=4.2, $fn=30);
  // Mod for 10mm bar
  translate([11,2,45]) rotate([0,90,90]) cylinder(h = 270, r=4.2, $fn=30); 
  // Ziptie
  translate([-5,10,37]) cube([30,3.5,2]);
  translate([-5,10,37]) rotate([45,0,0]) cube([30,1.42,1.42]);
 }
}

module corner_fancy(){
 // Side corner cutouts
  translate([-8,-9,0]) rotate([0,0,-45-180]) translate([-15,0,-1]) cube([30,30,51]);
  translate([8,-9,0]) rotate([0,0,45-180]) translate([-15,0,-1]) cube([30,30,51]);
 // Top corner cutouts
  translate([7,0,49-2]) rotate([0,45,0]) translate([-15,-15,0]) cube([30,30,30]);
  translate([-7,0,49-2]) rotate([0,-45,0]) translate([-15,-15,0]) cube([30,30,30]);
  rotate([0,0,90]){
   translate([-9,0,49-2]) rotate([0,-45,0]) translate([-15,-15,0]) cube([30,30,30]);
  }
}


// Final part
module corner(){
 // Rotate the part for better printing
 translate([0,0,11]) rotate([-90,0,0]) difference(){
  corner_base();
  corner_holes();
  corner_fancy();
 }
}

