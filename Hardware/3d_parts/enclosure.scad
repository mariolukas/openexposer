include <complete_view.scad>;

material_thickness = 5;

translate([-55,-98,120]) rotate([0,90,90]) side_wall();
translate([-55,98,120]) rotate([0,90,90]) side_wall();

translate([-185,0,-62.5])  bottom_plate();

module side_wall(){
   hull(){	
	translate([-140,180,0]) cylinder(material_thickness, 20,20,true );
	translate([160,-160,0]) cylinder(material_thickness, 20,20,true );

	translate([-140,-160,0]) cylinder(material_thickness, 20,20,true );
	translate([160,180,0]) cylinder(material_thickness, 20,20,true );
  }
}

module bottom_plate(){
	cube([100,208,5],true);
	cube([100,208,5],true);
}