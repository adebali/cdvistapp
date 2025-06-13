
    function saveSvgAsFile(id)
    {
        var mySvgObject = document.getElementById(id);	
        console.log(mySvgObject)
        var mySvg = $(mySvgObject).html();
        mySvg = '<svg  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" id="arc">' + mySvg + '</svg>'
        //var textToWrite = htmlString;
        var textFileAsBlob = new Blob([mySvg], {type:'svg'});
        var fileNameToSaveAs = "cdvist_domains.svg";

        var downloadLink = document.createElement("a");
        downloadLink.download = fileNameToSaveAs;
        downloadLink.innerHTML = "Download File";
        if (window.webkitURL != null)
        {
            // Chrome allows the link to be clicked
            // without actually adding it to the DOM.
            downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
        }
        else
        {
            // Firefox requires the link to be added to the DOM
            // before it can be clicked.
            downloadLink.href = window.URL.createObjectURL();
            downloadLink.onclick = destroyClickedElement;
            downloadLink.style.display = "none";
            document.body.appendChild(downloadLink);
        }

        downloadLink.click();
    }

function arr_diff(a1, a2) {
	let diff = new Set(a1)
	for (let i in a2) {
		let e2 = a2[i]
		for (let j in a1) {
			let e1 = a1[j]
			if (e1 === e2)
				diff.delete(e2)
		}
	}
	let differenceList = Array.from(diff)
	return differenceList
}

let domainsOverlap = function(start1, end1, start2, end2) {
	if ((start2 > start1 && start2 < end1) |
							(end2 > start1 && end2 < end1) |
							(start2 <= start1 && end2 >= end1) |
							(start2 >= start1 && end2 <= end1))
		return true
	return false
}

let sideOfOverlap = function(start1, end1, start2, end2) {
	let left,
		right = false
	if (domainsOverlap(start1, end1, start2, end2)) {
		if (start2 < start1)
			left = true

		if (end2 > end1)
			right = true

		if (left && right)
			return 'both'

		if (left)
			return 'left'

		if (right)
			return 'right'

		return 'inside'
	}
	return false
}

let filterLoop = function(entries, criterion) {
    filteredEntries = []
    entries.forEach(function(entry, entryNum) {
        newEntry = entry
        domains = entry.segments.assigned
        newEntry.segments.assigned = filterOverlappingHits(domains, criterion)
        filteredEntries.push(newEntry)
    })
    return filteredEntries
}

let addUnassigned = function(entries) {
    let newEntries = []
    entries.forEach(function(entry, entryNum) {
        let newEntry = entry
        newEntry.segments.assigned = newEntry.segments.assigned.concat(entry.segments.unassigned)
        console.log(newEntry)
        newEntries.push(newEntry)
    })
    console.log(newEntries)
    return newEntries
}

let polishDomainData = function(entries) {
    newEntries = []
    entries.forEach(function(entry, entryNum) {
        newEntry = entry
        newDomains = []
        domains = entry.segments.assigned
        domains.forEach(function(domain){
            if (domain.tool.name == 'hhsearch' & domain.tool.db.startsWith('pfam')) {
                domain.stroke = "rgba(155,0,0,1)"
                domain.name = domain.name.split(';')[1]
            }
            else if (domain.tool.name == 'hhsearch' & domain.tool.db.startsWith('pdb')) {
                domain.stroke = "rgba(155,0,0,1)"
                domain.name = domain.name.split(' ')[0].split('_')[0]
            }
            else if (domain.tool.name == 'hhsearch' & domain.tool.db.startsWith('scop')) {
                domain.stroke = "rgba(155,0,0,1)"
                domain.name = domain.name.split(' ')[0]
            }
            else if (domain.tool.name == 'rpsblast' & domain.tool.db.startsWith('scop')) {
                domain.stroke = "rgba(155,0,0,1)"
                domain.name = domain.name.split(' ')[0]
            }
            else {
                domain.stroke = "rgba(0,0,0,1)"
            }
            newDomains.push(domain)
        })
        newEntry.segments.assigned = newDomains
        newEntries.push(newEntry)
    })
    return newEntries
}

let filterOverlappingHits = function(domains, criterion) {
	if (domains === []) {
		return domains
    }

	let filteredDomains = []
	domains.forEach(function(domain1, index1, array1) {
		array1.forEach(function(domain2, index2, array2) {
			if (filteredDomains.indexOf(domain1) === -1 && filteredDomains.indexOf(domain2) === -1 ) {
				if (index1 !== index2) {
					let overlap = sideOfOverlap(domain1.start, domain1.end, domain2.start, domain2.end)
					// console.log(overlap)
					if (overlap) {
						if (domain1[criterion] > domain2[criterion])
							filteredDomains.push(domain2)
						if (domain1[criterion] < domain2[criterion])
							filteredDomains.push(domain1)
					}
				}
			}
		})
	})
	// console.log(filteredDomains)
	// console.log(filterDomains(domains, filteredDomains))
	console.log(domains)
	console.log(filteredDomains)
	return arr_diff(domains, filteredDomains)
}

function domainShowHide(probabilityCutoff) {
    d3.select('#probText').text('HHsearch Prob. >' + probabilityCutoff + '%')
    d3.selectAll('.domain').filter(function(d) {return (d.prob == null || d.prob >= probabilityCutoff)}).style('opacity', 1)
    d3.selectAll('.domain').filter(function(d) {return (d.prob != null && d.prob < probabilityCutoff)}).style('opacity', 0)
}

function hhsearchRun(tools) {
    let flag = false
    tools.forEach(function(tool) {
        if (tool.name == 'hhsearch') {
            flag = true
        }
    })
    return flag
}

function drawProbabilityCutoffBar() {
    
    let probabilityBarParagraph = d3.select('#probBar')
    
    // probabilityBarParagraph.append('b')
    //     .text('|')
    //     .style('vertical-align', 'bottom')
    
    probabilityBarParagraph.append('label')
        .style('vertical-align', 'bottom')
        .attr('id', 'probCutoffValue')

    let probText = probabilityBarParagraph.append('text')
        .text('HHsearch Prob. >60%')
        .attr('id', 'probText')
        .style('vertical-align', 'bottom')
        

    probabilityBarParagraph.append('input')
        .attr('class', 'form-control')
        .attr('type', 'range')
        .attr('min', '0')
        .attr('max', '100')
        .attr('step', '1')
        .attr('value', '60')
        .attr('data-orientation', 'vertical')
        .attr('oninput', 'domainShowHide(value)')
        .style('width', '300px')
        .style('display', 'inline-block')
        .style('vertical-align', 'bottom')
        

}

function drawFromFile(dataFile, filter=true, unassigned=false) {
    
    d3.json(dataFile, function(error, json) {
        if (error) return console.warn(error)
        
        if (hhsearchRun(json.tools)) {
            drawProbabilityCutoffBar()
        }

        if (filter) {
            data = filterLoop(json.entries, 'score')
        }
        else {
            if (unassigned) {
                data = addUnassigned(json.entries)
            }
            else {
                data = json.entries
            }
        }
        data = polishDomainData(data)
        drawFromData(data)
        domainShowHide(60)
    })
}



function drawFromData(data) {
    // Constants 
    let kSvgHeight = 100
    let kSvgLateralExtension= 1
    let kBackboneHeight = 10
    let kDomainHeight = 40
    let kDomainStrokeWidth = 3
    let kPartialPixel = 3
    let kTransmembraneHeight = 50
    let kCoilsHeight = 45
    let kLcrHeight = 45
    let kDomainTextMargin = 5
    let kNameLengthToPixelFactor = 10
    let kFontFamily = "Verdana"
    let kFontSize = 18
    let domainColors = {
        "domain"        : "rgba(255,255,255,0.8)",
        "domainStroke"  : "rgba(0,0,0,0.5)",
        "tm"            : "rgba(100,100,100,0.7)",
        "coils"         : "rgba(46,139,87,0.7)",
        "lcr"           : "rgba(199,21,133,0.7)"
    }

    // Computed constants
    let kMiddleY = kSvgHeight / 2
    let kBackboneYstart = kMiddleY - (kBackboneHeight/2)
    let kDomainYstart = kMiddleY - (kDomainHeight/2)
    let kDomainYend = kMiddleY + (kDomainHeight/2)
    let kTransmembraneYstart = kMiddleY - (kTransmembraneHeight/2)
    let kCoilsYstart = kMiddleY - (kCoilsHeight/2)
    let kLcrYstart = kMiddleY - (kLcrHeight/2)

    function domainBorder(d, cov = '[]') {
        partialPixelLeft = cov[0] === '[' ? 0 : kPartialPixel
        partialPixelRight = cov[1] === ']' ? 0 : kPartialPixel
        let kQuarterDomainHeight = kDomainHeight/4

        pathList = [ 
            { "x": d.start, "y": kDomainYstart},
            { "x": d.end, "y": kDomainYstart},
            { "x": d.end - partialPixelRight, "y": kDomainYstart + kQuarterDomainHeight},
            { "x": d.end, "y": kDomainYstart + kQuarterDomainHeight*2},
            { "x": d.end - partialPixelRight, "y": kDomainYstart + kQuarterDomainHeight*3},
            { "x": d.end, "y": kDomainYstart + kDomainHeight},
            { "x": d.start, "y": kDomainYend},
            { "x": d.start + partialPixelLeft, "y": kDomainYend - kQuarterDomainHeight},
            { "x": d.start, "y": kDomainYend - kQuarterDomainHeight*2},
            { "x": d.start + partialPixelLeft, "y": kDomainYend - kQuarterDomainHeight*3},
            { "x": d.start, "y": kDomainYend - kDomainHeight}
        ]
        let path =  ' M ' + pathList[0].x + ' ' + pathList[0].y + 
                    ' L ' + pathList[1].x + ' ' + pathList[1].y +
                    ' L ' + pathList[2].x + ' ' + pathList[2].y +
                    ' L ' + pathList[3].x + ' ' + pathList[3].y +
                    ' L ' + pathList[4].x + ' ' + pathList[4].y + 
                    ' L ' + pathList[5].x + ' ' + pathList[5].y + 
                    ' L ' + pathList[6].x + ' ' + pathList[6].y + 
                    ' L ' + pathList[7].x + ' ' + pathList[7].y + 
                    ' L ' + pathList[8].x + ' ' + pathList[8].y + 
                    ' L ' + pathList[9].x + ' ' + pathList[9].y + 
                    ' L ' + pathList[10].x + ' ' + pathList[10].y +
                    ' Z'
        return path
    }


    // Create a table
    let table = d3.select('body')
        .style('margin', '0.5%')
        .append('div')
        .attr('id', 'main_svg')
        .style('width', '100%')
        .style('height', '100%')
        .append('table')
        .attr('id', 'domain_table')
        .style('table-layout', 'fixed')
        .style('width', '100%')
        
    let tableHead = table.append('thead').append('tr')

    tableHead.append('th')
        .style('width', '30%')
        // .text('Query Header')
        .text('')
    
    let secondColumHead = tableHead.append('th')
        // .text('Domain Architecture')
        .text('')

    let thirdColumHead = tableHead.append('th')
        // .text('Domain Architecture')
        .style('width', '5%')        
        .text('')



    let row = table.selectAll()
        .data(data)
        .enter()
        .append('tr')

    // First column to place name
    let nameColum = row.append('td')
        .style('word-wrap', 'break-word')
        .style('font-family', kFontFamily)
        .style('font-size', kFontSize*.8)
        .text(function(d) { return d.header ? d.header : ''})

    // Second column for the main architecture SVG
    let architectureCell = row.append('td')
    let architecture = architectureCell.append('svg')
        .attr("id", function(d){return 'hey'})
        .attr("height", kSvgHeight)
        .attr("width", function(d) {return d.length ? d.length : 0 + kSvgLateralExtension})
        .append('g')
    
    let downloadCell = row.append('td')
    // downloadCell.append('p')
    //     .text('SVG')
    //     .attr('onclick', 
    //         function(d) {
    //         saveSvgAsFile('hey')
    //         // console.log(d.header.replace(/[!\"#$%&'\(\)\*\+,\.\/:;<=>\?\@\[\\\]\^`\{\|\}~]/g, ''))
    //         return 'console.log("Save SVG")'
    //         })
     

    function domainToFeaturesTable(d) {
        console.log(d)
        return `<table class='info'>
        <tr><td><b>Name</b></b></td><td>` + d.name + `</td></tr>
        <tr><td><b>Score</b></td><td>` + d.score + `</td></tr>
        <tr><td><b>Start</b></td><td>` + d.start + `</td></tr>
        <tr><td><b>End</b></td><td>` + d.end + `</td></tr>
        <tr><td><b>Prob</b></td><td>` + d.prob + `</td></tr>
        <tr><td><b>Coverage</b></td><td>` + d.cov + `</td></tr>
        <tr><td><b>Tool Name</b></td><td>` + d.tool.name + `</td></tr>
        <tr><td><b>Database</b></td><td>` + d.tool.db + `</td></tr>
        </table>`
    }
    
    // Draw backbone
    architecture.append('g')
        .filter(function(d){ return d.length && d.length>0 })
        .append('rect')
        .attr("x", 1)
        .attr("y", kBackboneYstart)
        .attr("width", function(d) { return d.length})
        .attr("height", kBackboneHeight)
        .attr("fill", "gray")

    architecture.each(function(d, i) {

        // Draw coiled coils
        let coils = d3.select(this).selectAll('svg')
            .data(d.coils ? d.coils:[])
            .enter()
            .append('g')
            .attr('class', 'coils')                        
            .filter(function(d){ return d.end - d.start > 0 })                
            .append('rect')
            .attr("x", function(d) { return d.start })
            .attr("y", kCoilsYstart)
            .attr("width", function(d) { 
                return d.end-d.start
            })
            .attr("height", kCoilsHeight)
            .attr("fill", domainColors.coils)

        // Draw coiled low-complexity regions
        let lcr = d3.select(this).selectAll('svg')
            .data(d.lcr ? d.lcr:[])
            .enter()
            .append('g')
            .attr('class', 'lcr')            
            .filter(function(d){ return d.end - d.start > 0 })
            .append('rect')
            .attr("x", function(d) { return d.start })
            .attr("y", kLcrYstart)
            .attr("width", function(d) { 
                return d.end-d.start
            })
            .attr("height", kLcrHeight)
            .attr("fill", domainColors.lcr)

        // Draw transmembrane regions
        // let tm = d3.select(this).selectAll('svg')
        //     .data(d.tm ? d.tm:[])
        //     .enter()
        //     .append('g')
        //     .attr('class', 'tm')
        //     .append('rect')
        //     .filter(function(d){ return d[1] - d[0] > 0 })
        //     .attr("x", function(d) { return d[0] })
        //     .attr("y", kTransmembraneYstart)
        //     .attr("width", function(d) { 
        //         return d[1]-d[0]
        //     })
        //     .attr("height", kTransmembraneHeight)
        //     .attr("fill", domainColors.tm)

        let tmr = d3.select(this).selectAll('svg')
            // .data(d.tm.domains[0] || [])
            .data(Array.isArray(d.tm) && d.tm[0] ? d.tm[0].domains : [])
            // .data(d.domains)
            .enter()
            .append('g')
            .attr('class', 'tm')
            .append('rect')
            .filter(function(d){ return d[1] - d[0] > 0 })
            .attr("x", function(d) { return d[0] })
            .attr("y", kTransmembraneYstart)
            .attr("width", function(d) { 
                return d[1]-d[0]
            })
            .attr("height", kTransmembraneHeight)
            .attr("fill", domainColors.tm)
        
        // Draw protein domains
        let domain = d3.select(this).selectAll('svg')
            .data(d.segments.assigned)
            // .data(d.segments.assigned ? filterOverlappingHits(d.segments.assigned, 'score') : [])
            .enter()
            .append('g')
            .attr('class', 'domain')

        // domain.append('rect')
        //     .filter(function(d){ return d.end - d.start > 0 })
        //     .attr("x", function(d) { return d.start })
        //     .attr("y", kDomainYstart)
        //     .attr("width", function(d) { 
        //         return d.end-d.start
        //     })
        //     .attr("height", kDomainHeight)
        //     .attr("fill", d.color ? d.color : domainColors.domain)
        //     .attr("stroke", d.stroke ? d.stroke : domainColors.domainStroke)
        //     .attr("stroke-width", 0)
        
        // Draw domain borders
        domain.append('path')
            .filter(function(d){ return d.end - d.start > 0 })
            .attr("d", function(d) { return domainBorder(d, d.cov ? d.cov : '[]') })
            .attr("stroke", function(d) { return d.stroke ? d.stroke : domainColors.domainStroke })
            .attr("stroke-width", kDomainStrokeWidth)
            .attr("fill", function(d) { return d.color ? d.color : domainColors.domain })
            .attr("stroke-linecap", "round")

        // Name the domain
        domain.append('text')
            .filter(function(d){ return (d.end - d.start > 0) && d.name })
            .attr("x", function(d) {return (d.start+d.end)/2 })
            .attr("y", kMiddleY)
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "central")
            .attr("textLength", function(d) { return Math.max(1, Math.min(d.name.length*kNameLengthToPixelFactor, d.end-d.start-(kDomainTextMargin*2))) })
            .attr("font-family", kFontFamily)
            .attr("font-size", kFontSize)
            .attr("lengthAdjust", "spacingAndGlyphs")
            .text(function(d) { return d.name})


            
        domainArea = domain.append('rect')
            .filter(function(d){ return d.end - d.start > 0 })
            .attr("x", function(d) { return d.start })
            .attr("y", kDomainYstart)
            .attr("width", function(d) { 
                return d.end-d.start
            })
            .attr("height", kDomainHeight)            
            .style("opacity", 0)
            
            domainArea.on("click", function (d) {
                if (d.active) {
                    d3.select("body").select('div.tooltip').remove();
                    d.active = false
                }
                else {
                    d3.select("body").select('div.tooltip').remove();                    
                    var g = d3.select(this); // The node
                    var div = d3.select("body").append("div")
                            .attr('pointer-events', 'none')
                            .attr("position", "absolute")
                            .attr("class", "tooltip")
                            // .style("opacity", 1)
                            .html("<hr>" + domainToFeaturesTable(d) + " <hr>")
                            .style("left", ("100px"))
                            .style("top", ("100px"))

                    d3.select('info')
                        .style('margin', '10px')
                    d.active = true
                }
            })
    
            // domainArea.on("mouseout", function (d) {
            //     d3.select("body").select('div.tooltip').remove();
            // })
    })

    scaleRow = table.append('tr')
    scaleRow.append('td')
    scaleSvg = scaleRow.append('td').append('svg')

    scaleSvg.append('g')
        .append('rect')
        .attr("x", 1)
        .attr("y", kBackboneYstart)
        .attr("width", 100)
        .attr("height", kBackboneHeight / 2)
        .attr("fill", "black")
    
    scaleSvg.append('g')
        .append('text')
        .attr("x", 50)
        .attr("y", kMiddleY - kSvgHeight/4)
        .attr("text-anchor", "middle")
        .attr("alignment-baseline", "central")
        .attr("font-family", kFontFamily)
        .attr("font-size", kFontSize)
        .attr("lengthAdjust", "spacingAndGlyphs")
        .text('100 aa')

}