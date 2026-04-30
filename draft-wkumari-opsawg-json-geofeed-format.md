---
title: "A JSON Format for Self-Published IP Geolocation Feeds"
abbrev: "JSON Geofeed Format"
category: info
updates: RFC8805

docname: draft-wkumari-opsawg-json-geofeed-format-latest
submissiontype: IETF  # also: "independent", "editorial", "IAB", or "IRTF"
number:
date:
consensus: true
v: 3
area: "Operations and Management"
workgroup: "Operations and Management Area Working Group"
keyword:
 - geofeed
 - geolocation
 - ip geolocation
 - json
venue:
  group: "Operations and Management Area Working Group"
  type: "Working Group"
  mail: "opsawg@ietf.org"
  arch: "https://mailarchive.ietf.org/arch/browse/opsawg/"
  github: "wkumari/draft-wkumari-opsawg-json-geofeed-format"
  latest: "https://wkumari.github.io/draft-wkumari-opsawg-json-geofeed-format/draft-wkumari-opsawg-json-geofeed-format.html"

author:
 -
    fullname: "Warren Kumari"
    organization: Google LLC
    email: "warren@kumari.net"

normative:
  RFC8805:

informative:
  IAB-IP-GEO:
      title: "Report from the IAB Workshop on IP Address Geolocation"
      author:
        - name: J. Iyengar
        - name: J. Livingood
        - name: T. Pauly
      date: 2026-04-08
  KLINE-GEO:
    title: "Anecdotal History of RFC 8805"
    author:
      - name: E. Kline
    date: 2025-11
    target: "https://www.ietf.org/slides/slides-ipgeows-paper-anecdotal-history-of-rfc-00.pdf"
  SZAMONEK-GEO:
    title: "The Need for an Alternative to IP-Based Geolocation"
    author:
      - name: Z. Szamonek
    date: 2025-11
    target: "https://www.ietf.org/slides/slides-ipgeows-paper-the-need-for-an-alternative-to-ip-based-geolocation-00.pdf"
...

--- abstract

This document defines a JavaScript Object Notation (JSON) format for self-published IP geolocation feeds. It updates RFC 8805 by transitioning from the current comma-separated values (CSV) format to a more expressive JSON format, addressing the need for operational extensibility.


--- middle

# Introduction

{{RFC8805}} Section 2.1 defines a CSV-based format for network operators to
publish a mapping of IP address prefixes to simplified geolocation information.
While widely deployed, the authors of {{RFC8805}} acknowledged in Section 7that
the CSV format has "extremely limited extensibility" and that future work
should involve the development of a more expressive format, specifically
suggesting JSON (see{{RFC8805}}, Section 7. "Planned Future Work").

Furthermore, {{IAB-IP-GEO}} identified several critical gaps in the existing
geofeed ecosystem, including:

* The CSV format cannot adequately express varying levels of confidence in a
location mapping ({{IAB-IP-GEO}}, Section 4.2), nor can it map a prefix
to multiple locations ({{IAB-IP-GEO}}, Section 5.2) for example if the prefix is used for Anycast.

* The current format lacks the ontology to clarify whether the geolocation
mapping refers to the physical location of the user, the location of network
infrastructure, a network egress point, or a regulatory jurisdiction ({{IAB-IP-GEO}},
Section 3.3).

Note that {{IAB-IP-GEO}} also identified other, more architectural issues,
including that physical location does not necessarily correspond to network
topologies, the lack of user consent mechanisms, the potential for privacy
violations, the need for different levels of precision (e.g. "get me to a close
datacenter" vs "the ambulance needs my physical address", etc).

However, these issues, while very important, are orthogonal to the data format
and should be addressed through other mechanisms. This document simply tries to
improve the data format to better support the ecosystem as it currently exists,
while providing a framework for future extensions.

Readers are strongly encouraged to read {{IAB-IP-GEO}}, the accompanying papers from the
IAB Workshop on IP Address Geolocation for a deeper understanding of these
architectural issues and the broader context of geolocation in the modern
internet. {{KLINE-GEO}} and {{SZAMONEK-GEO}} are particularly recommended to
understand the architecture, use-case and privacy considerations in the
original design.

This document defines defines a new JSON-based format to address the
extensibility limitations of the current CSV format, while maintaining
compatibility with the core fields defined in {{RFC8805}}. It also introduces
new fields to address some of the gaps identified in {{IAB-IP-GEO}}.

# Conventions and Definitions

{::boilerplate bcp14-tagged}

# JSON Geofeed Format

The JSON format for geolocation feeds builds upon the fields
specified in RFC 8805: IP prefix, alpha2code, region, city.

Note that, as {{RFC8805}} deprecated the use of the postal code field ({{RFC8805}}, Section 2.1.1.5 - "Postal Code"), the JSON
format does not support it.

A JSON geofeed MUST be an array of JSON objects.

Each object MUST contain the following keys:

* **ip_prefix**: same semantics as defined in {{RFC8805}}
*  **alpha2code**: same semantics as defined in {{RFC8805}}
*  **region**: same semantics as defined in {{RFC8805}}
* **city**: same semantics as defined in {{RFC8805}}

In addition, each object MUST contain:

 * **last_updated**: A string indicating the timestamp of the last update to that record, formatted as an ISO 8601 date-time. This field is critical for consumers to assess the freshness of the data, given the dynamic nature of IP address allocations and network changes.

Objects MAY contain the following optional keys:

* **location_type** (optional): A string indicating the nature of the location.
*  Valid
  values include `infrastructure`, `network_egress`, `organization` and `jurisdiction`.

* **confidence** (optional): A string expressing the certainty level of
  the mapping ({{IAB-IP-GEO}}, Section 5.2). Valid values include `high`, `medium`, and `low`.


Example JSON Geofeed Entry:

~~~~

[
  {
    "ip_prefix": "192.0.2.0/24",
    "alpha2code": "US",
    "region": "US-AL",
    "city": "Alabaster",
    "location_type": "infrastructure",
    "confidence": "high",
    "last_updated": "2024-06-01T12:00:00Z"
  },
  {
    "ip_prefix": "198.51.100.0/24",
    "alpha2code": "CZ",
    "region": "CZ-PR",
    "city": "Praha",
    "location_type": "network_egress",
    "confidence": "medium",
    "last_updated": "2017-07-01T12:00:00Z"
  }
]

~~~~

The `location_type` field allows publishers to clarify the context of the
geolocation mapping, while the `confidence` field provides a mechanism to
express the reliability of the data. The `last_updated` field helps consumers
assess the freshness of the information, which is crucial given the dynamic
nature of IP address allocations and network changes.

{**Editor note**: Multiple people have suggested new fields
that should be added to the format, but we need to be careful about scope
creep. These are only some of the proposed fields, but any others such as
`source`, `accuracy_radius` and `access_technology` have also been discussed.
For example, `access_technology` would be used to indicate the type of network
access, such as `wifi`, `cellular`, or `ethernet`, and / or `speed`, `jitter`,
etc.

I have intentionally kept the initial list the same as RFC8805, but added
`last_updated` as it was obviously needed, and  `location_type` and
`confidence` as examples.

There will need to be careful discussion of other potential fields before they
are added to the format, and it is possible that there will need to be a
dedicated venue for such discussions. In addition, we might consider creating a
registry for these fields to ensure consistency and interoperability, and a
mechanism to provide "private" extensions.}


# Security Considerations

As noted in RFC 8805, self-publication of location data opens no new attack
vectors, but consumers must validate inputs from potentially hostile sources.

The JSON format allows for greater specificity, which increases the necessity for publishers to verify they have operational authority over the advertised prefixes and to ensure the accuracy of the geolocation data. Consumers should also be aware of the potential for stale data and consider the `last_updated` field when making decisions based on geofeed information.

# IANA Considerations

This document has no IANA actions.


--- back

# Acknowledgments
{:numbered="false"}

The authors would like to thank the participants of the IAB Workshop on IP
Address Geolocation for their valuable insights and feedback, which have
greatly informed the development of this document.

In particular, the authors would like to thank the following individuals for
their contributions to the discussions that led to the development of this
document: Nimrod Levy, Jari Arkko, Brian Trammell, Erik Kline, Erik Nygren,
Geoff Huston, Jari Arkko, Jason Livingood, Joe Abley, Joe Clarke, Joel Jaeggli,
Jana Iyengar, Lee Howard, Robert Kisteleki, Tommy Pauly,
```

# Appendix A: Example Conversion Script
{:numbered="false"}

The following Python program (convert.py) demonstrates how to convert an RFC 8805 format CSV geofeed into the JSON format defined in this document. This script reads from standard input and outputs the JSON to standard output.

Note that this is a simple example script and does not include error handling, validation, or support for all potential fields. It is intended for illustrative purposes only.

--- CODE BEGINS ---

~~~~
{::include code/convert.py}
~~~~

--- CODE ENDS ---

The following Python program (test_convert.py) includes unit tests for the conversion script, demonstrating how to test the conversion of CSV input into the expected JSON output.

--- CODE BEGINS ---

~~~~
{::include code/test_convert.py}
~~~~

--- CODE ENDS ---

