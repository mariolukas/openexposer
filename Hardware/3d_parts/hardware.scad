//Hardware objects such as bearings and motors
//defined here for convenience

//Mark Benson - April 2013
//
// CC - GNU


//Define generic, configurable module to generate a 'bearing'
module bearing(outerRaceSize, innerRaceSize, thickness)
{
	difference()
	{	
		cylinder(r=outerRaceSize/2, h=thickness);
		cylinder(r=innerRaceSize/2, h=thickness);
	}
}

//Now define bearing module with real world parameters

//Predefined 608 Bearing
module bearing608()
{
	bearing(22, 8, 7);
}

//Predefined 624 Bearing
module bearing624()
{
	bearing(13, 4, 5);
}

//Predefined 626 Bearing
module bearing626()
{
	bearing(19, 6, 6);
}

//Predefined LM8UU Bearing
module bearingLM8UU()
{
	bearing(15, 8, 24);
}

//Test bearing modules
//Uncomment line(s) below to test
//
//Note: Translations allow all bearings to shown at the same time
//rather than being on top of each other

//translate([0,0,0]) bearing624();
//translate([0,20,0]) bearingLM8UU();
//translate([0,43,0]) bearing626();
//translate([0,70,0]) bearing608();




// ** STEPPER MOTORS **
//
//
//Define a generic stepper motor module

module stepperMotor(caseSize, caseHeight, holeSpacing, holeDiameter, shaftDiameter, shaftHeight, shaftCollarDiameter, shaftCollarThickness)
{
	
	//Mounting Hole Depth is predefined @ >= 4.5mm
	mountingHoleDepth = 4.5;

	union()
	{

		//Shaft
		//Note: We add 1mm and translate to -1 in Z to show shaft 
		//on bottom of motor
		translate([caseSize/2,caseSize/2,-1]) 
		cylinder(r=shaftDiameter/2, h=caseHeight+shaftHeight+1);	

		//Shaft collar
		translate([caseSize/2,caseSize/2,caseHeight]) 
		cylinder(r=shaftCollarDiameter/2, h=shaftCollarThickness);

		difference()
		{
			cube([caseSize, caseSize, caseHeight]);
		
			translate([(caseSize-holeSpacing)/2,(caseSize-holeSpacing)/2,caseHeight-mountingHoleDepth]) 
			cylinder(r=holeDiameter/2, h=mountingHoleDepth);

			translate([caseSize-((caseSize-holeSpacing)/2),(caseSize-holeSpacing)/2,caseHeight-mountingHoleDepth]) 
			cylinder(r=holeDiameter/2, h=mountingHoleDepth);

			translate([(caseSize-holeSpacing)/2,caseSize-((caseSize-holeSpacing)/2),caseHeight-mountingHoleDepth]) 
			cylinder(r=holeDiameter/2, h=mountingHoleDepth);

			translate([caseSize-((caseSize-holeSpacing)/2),caseSize-((caseSize-holeSpacing)/2),caseHeight-mountingHoleDepth]) 
			cylinder(r=holeDiameter/2, h=mountingHoleDepth);
		}
	}
	
}


//Define stepper motor with real world parameters

//Predefined NEMA14 stepper motor
module nema14()
{
	stepperMotor(35.2, 36, 26.0, 3, 5, 24, 22, 2);
}


//Predefined NEMA17 stepper motor
module nema17()
{
	stepperMotor(42, 48, 31, 3, 5, 24, 22, 2);
}


//Test stepper motors
//Note: Translations allow all objects to appear on screen together
//rather than being shown one on top of the other
//translate([20,0,0]) nema14();
//translate([20,50,0]) nema17();