/**
 * NEMAMount.scad
 *
 * Produces the shape to be subtracted from a base to make a NEMA motor mount.
 *
 * @copyright  James Newton, 2013
 * @license    http://creativecommons.org/licenses/LGPL/2.1/
 * @license    http://creativecommons.org/licenses/by-sa/3.0/
 *
 * @see        http://www.thingiverse.com/thing:137829
 *
 *
**/


/* ******************************************************************************
 * Customizer parameters and rendering
 * ****************************************************************************** */

/* [Global] */


//The NEMA size. See: massmind.org/techref/io/stepper/nemasizes.htm
NEMA_Size = 17; // [8,11,14,17,23,34,42]

//Drive Shaft clearance hole: 0=no shaft, positive # = that size, negative number = standard NEMA shaft + abs(shaft) e.g. NEMA_Mount(17,shaft=-1) gives a 5+1=6mm shaft hole.
shaft = -1; // [-50:50]

//Pilot mounting indentation diameter: 0=no indentation, positive # = that diameter, negative # = standard NEMA pilot + abs(pilot)
pilot = -1; // [-20:90]

//height of the mounting and shaft holes. e.g. the thickness of your mounting plate
height = 10; // [1:100]

//Size of nut head. 0 for no nuts or an M size.
nut_size = 4; // [0:20]

//height of the nut head. 0 for no nuts or an M height.
nut_height =3; // [0:20]

//Distance the motor can slide in the mount.
adjust = 5; // [0:10]

//Show sample base with NEMA mount subtracted.
Show_Base =  0; // [0,1]

/* [Hidden] */


/*
difference() {
	if (Show_Base==1)
		translate([-NEMA_Size*2,-NEMA_Size*2,0]) cube([NEMA_Size*4,NEMA_Size*4,height-.01]);
	NEMA_Mount (NEMA_Size, shaft, pilot, height, nut_size, nut_height, adjust);
	}

*/

module NEMA_Mount (NEMA_Size, shaft=-1, pilot=-1, height, nut_size, nut_height, adjust=0) {
	for (r = [-adjust: 2: adjust]) 
		translate([r,0,0])
		Simple_NEMA_Mount (NEMA_Size, shaft, pilot, height, nut_size, nut_height, $fs=adjust/2+0.01);
	//drop the resolution to keep from swamping the system with CSG Products.
	}

module Simple_NEMA_Mount (NEMA_Size, shaft=-1, pilot=-1, height, nut_size, nut_height) {

	NEMA_Mount = lookup(NEMA_Size,[
		[ 8,15.4/2],
		[11,23.0/2],
		[14,26.0/2],
		[17,31.04/2],
		[23,47.14/2],
		[34,69.58/2],
		[42,88.90/2]
		]);

	NEMA_Bolt = lookup(NEMA_Size,[
		[ 8,2.0/2],
		[11,2.5/2],
		[14,3.0/2],
		[17,4.0/2],
		[23,4.75/2],
		[34,6.5/2],
		[42,7.15/2]
		]);

//the -.1's here are to ensure the hole breaks through the mounting plate
	translate([-NEMA_Mount,-NEMA_Mount,-.1]) cylinder(h=height-nut_height+.2, r=NEMA_Bolt);
	if (nut_height > 0) translate([-NEMA_Mount,-NEMA_Mount,height-nut_height]) nut(nut_size, nut_height);
	translate([-NEMA_Mount,+NEMA_Mount,-.1]) cylinder(h=height-nut_height+.2, r=NEMA_Bolt);
	if (nut_height > 0) translate([-NEMA_Mount,+NEMA_Mount,height-nut_height]) nut(nut_size, nut_height);
	translate([+NEMA_Mount,-NEMA_Mount,-.1]) cylinder(h=height-nut_height+.2, r=NEMA_Bolt);
	if (nut_height > 0) translate([+NEMA_Mount,-NEMA_Mount,height-nut_height]) nut(nut_size, nut_height);
	translate([+NEMA_Mount,+NEMA_Mount,-.1]) cylinder(h=height-nut_height+.2, r=NEMA_Bolt);
	if (nut_height > 0) translate([+NEMA_Mount,+NEMA_Mount,height-nut_height]) nut(nut_size, nut_height);
	if (shaft > 0) translate([0,0,-.1]) cylinder(h=height+.1, r=shaft);
	if (shaft < 0) translate([0,0,-.1]) cylinder(h=height+.1, r=-shaft + lookup(NEMA_Size,[
		[ 8,4.00/2],
		[11,5.00/2],
		[14,5.00/2],
		[17,5.00/2],
		[23,6.35/2],
		[34,9.50/2],
		[42,16.0/2]
		])
		);
	if (pilot > 0) cylinder(h=2, r=pilot);
	if (pilot < 0) translate([0,0,-.1]) cylinder(h=2, r=-pilot + lookup(NEMA_Size,[
		[ 8,15.00/2],
		[11,22.00/2],
		[14,22.00/2],
		[17,22.00/2],
		[23,38.10/2],
		[34,73.00/2],
		[42,73.0/2]
		])
		);
	};

module nut(nutSize,nutHeight) {
	//I have no idea if this actually produces the correct size.
	// need to check against:
	//http://www.boltdepot.com/fastener-information/Nuts-Washers/Metric-Nut-Dimensions.aspx
	for (r = [-60, 0, 60]) 
		translate([0,0,nutHeight/2]) rotate([0,0,r]) cube([nutSize*1.75, nutSize, nutHeight], true);
	}

