<!--
This file is part of PyPop

  Copyright (C) 2003. The Regents of the University of California (Regents) 
  All Rights Reserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
USA.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS,
ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF
REGENTS HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF
ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". REGENTS HAS NO OBLIGATION
TO PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
MODIFICATIONS.
-->
<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="lib.xsl"/>
 <!-- select "text" as output method -->
 <xsl:output method="xml" encoding="utf8" omit-xml-declaration="yes"/>

 <xsl:param name="two-en" select="0"/>
 <xsl:param name="k" select="0"/>

 <!-- override for the moment -->
 <xsl:template name="newline"/>

 <!-- unique key for all loci -->
 <xsl:key name="loci" match="/meta/dataanalysis/locus" use="@name"/>

 <xsl:template match="/">
  <xsl:call-template name="sort-by-locus"/>
 </xsl:template>

 <xsl:template name="sort-by-locus">

  <xsl:variable name="names"
   select="/meta/dataanalysis/locus[generate-id(.)=generate-id(key('loci',@name))]"/>

  <xsl:element name="output">
   <xsl:attribute name="sorted-by">locus</xsl:attribute>

   <xsl:for-each select="$names">

   <xsl:element name="locus">
    <xsl:attribute name="name">
     <xsl:value-of select="@name"/>
    </xsl:attribute>

    <xsl:call-template name="newline"/> 

    <xsl:for-each select="key('loci',@name)">
     <xsl:message><xsl:value-of select="allelecounts/allelecount"/> <xsl:value-of select="$two-en"/></xsl:message>
     <xsl:if test="allelecounts/allelecount &gt;= $two-en and allelecounts/distinctalleles &gt;= $k">
     <xsl:element name="population">
      <xsl:call-template name="newline"/> 

      <xsl:element name="popname">     
       <xsl:value-of select="../populationdata/popname"/>
      </xsl:element>
      <xsl:call-template name="newline"/>

      <xsl:element name="filename">     
       <xsl:value-of select="../filename"/>
      </xsl:element>
      <xsl:call-template name="newline"/>

      <xsl:copy-of select="*"/>
      <xsl:call-template name="newline"/>

     </xsl:element>
     <xsl:call-template name="newline"/>
     </xsl:if>
    </xsl:for-each>
   </xsl:element>
   <xsl:call-template name="newline"/>

  </xsl:for-each>

  </xsl:element>

 </xsl:template>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
