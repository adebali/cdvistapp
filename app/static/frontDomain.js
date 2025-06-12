'use strict'

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

let filterOverlappingHits = function(domains, criterion) {
	if (domains === [] | domains[0][criterion] === 'undefined') {
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

