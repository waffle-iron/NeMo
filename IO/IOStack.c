//
// Created by Mark Plagge on 5/25/16.
//

#include "IOStack.h"


FILE * inputFile;
bool inputFileOpen;
int start[2], stride[2], count[2], block[2];








/** Currently, initInFiles and subsequently NeMo expect a single file per 
 *  MPI Rank. The preprocessor script should create a file per rank for input.
 *  Eventually, this could be migrated to having a single binary file read through
 * collective MPI IO. */
void initInFiles(int startLoc, int endLoc){
    
}


void saveEvent(tw_stime timestamp, char sourceType, id_type core, id_type local,
               id_type destCore, id_type destLocal){
	

	
}

