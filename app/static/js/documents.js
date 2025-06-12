

function tooltips()
{

var documents = {};
documents["TMprediction"] = "Transmembrane Prediction: <br> Transmembrane regions are predicted and represented on the sequence backbone at scaled positions";
documents["TMHMM"] = "Transmembrane Hidden Markov Model:<br> A widely used TM prediction tool.";
documents["phobius"] = "PHOBIUS: <br> Yet another TM prediction tool that helps in discriminating TM regions from N-signal region. ";
documents["HMMsearch"] = "HMMER3: <br> Highly specific domain search tool. Algorithm aligns query sequence with HMMs of Pfam-A 29.0 database. <br> If it is turned off, CDvist will skip this step.";
documents["rpsblast"] = "Reverse PSI-BLAST: <br> Compares query with the pre-computed Position Specific Score Matrices (PSSMs) from Conserved Sequence Database (CDD)";
documents["evalue"] = "RPS-BLAST E-value: If there is a hit with E-value lower than this threshold, the best hit is recorded as significant hit.<br> After significant hit found, domain architecture is updated and the same method is re-applied for newly generated untagged subsequences. <br> If it is turned off, CDvist will skip this step.";
documents["domain_split"] = "Domain split: <br> If there is a significant unaligned region between hit and query, this function splits the hit and leaves unaligned regions untagged. <br> This allows user to discover potential domains within the current domain model. <br> By default if 5% of the covered query is not aligned with the hit, it is splited. However, user can change this value.";
documents["HHsearch"] = "HHsearch: <br> Compares either query sequence or query hmm profile with database profiles. First it tries aligning the raw sequence with the HMMs against selected database (sequence-profile search).<br> If there is no hit above the probability threshold and if HHblits option is on, it runs HHblits to generate query HMM which is searched through the HMM database via profile-profile alignment.";
documents["HHblits"] = "HHblits: Similarity search (2 iterations) against Uniprot and/or non-redundant databases which produces an alignment. The alignment is converted into profile and HHsearch is performed on the user-determined databases.<br> ";
documents["pfam"] = "Protein Families (PFAM) <br>";
documents["cdd"] = "Conserved Domain Database (CDD) <br>";
documents["pdb"] = "Protein Data Bank (PDB) <br>";
documents["cog"] = "Clustered of Orthologous Groups (COG) database <br>";
documents["scop"] = "Structural Classification of Proteins (SCOP) database <br>";
documents["smart"] = "Simple Modular Architecture Research Tool (SMART) database <br>";
documents["tigr"] = "TIGR Plant Transcript Assemblies database<br>";
documents["pirsf"] = "Protein Information Resource Super Familiy <br>";
documents["nr"] = "Non-redundant (NR) database <br>";
documents["uniprot"] = "Uniprot database<br>";
documents["both"] = "Uniprot and NR databases respectively. If no significant hit is found through Uniprot, HHblits will run against NR <br>";
documents["probability"] = "Probability cutoff for HHsearch. The best hit above this value will be considered as significant and domain architecture will be updated .<br>";
documents["gap"] = "Gap Length cutoff. Orphan protein segments shorter than this value will be ignored for domain search. (Minimum is 10, default is 30)<br>";
documents["rps_evalue"] = "E-value cutoff for RPS-BLAST.<br> The best hit lower than this value will be used to tag the corresponding sequence.<br>";
documents["hhblits_none"] = "If selected, no HMM-HMM search will be performed. <br>";
documents["hhblits_probability"] = "After HMM-HMM search, the best hit above this cutoff will be the significant hit. <br>";



// for (key in documents){
	// console.log(key);
	// d3.selectAll("." + key)
	// .attr("title",documents[key]);
	// $("." + key).tooltip({placement : 'top',events: {tooltip: "click,mouseleave"}, effect: 'slide'});
	// }

	
for (key in documents){
	//console.log(key);
	$('a.' + key).aToolTip({
		
		clickIt: true,
		tipContent: documents[key] 
	});
	}
	
	
    $('a').aToolTip({  
        // no need to change/override  
        closeTipBtn: 'aToolTipCloseBtn',  
        toolTipId: 'aToolTip',  
        // ok to override  
        fixed: true,                   // Set true to activate fixed position  
        clickIt: true,                 // set to true for click activated tooltip  
        inSpeed: 200,                   // Speed tooltip fades in  
        outSpeed: 100,                  // Speed tooltip fades out  
        tipContent: '',                 // Pass in content or it will use objects 'title' attribute  
        toolTipClass: 'defaultTheme',   // Set class name for custom theme/styles  
        xOffset: 5,                     // x position  
        yOffset: 5,                     // y position  
        onShow: null,                   // callback function that fires after atooltip has shown  
        onHide: null                    // callback function that fires after atooltip has faded out      
    });  
	

// $(function() {
    // $( document ).tooltip();
  // });
	
}

