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
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exsl="http://exslt.org/common"
 xmlns:str="http://exslt.org/strings"
 extension-element-prefixes="exsl str">

 <xsl:import href="lib.xsl"/>

 <xsl:output method="text" omit-xml-declaration="yes"/>

 <xsl:template match="text()"/>

 <xsl:template match="/">
  <xsl:apply-templates/>
 </xsl:template>


 <xsl:template match="emhaplofreq/group[(string-length(@loci) -
 string-length(translate(@loci, ':', '')))=2 and @role!='no-data']"> 


  <xsl:variable name="loci-array" select="str:tokenize(@loci, ':')"/>


  <xsl:variable name="first" select="$loci-array[1]"/>
  <xsl:variable name="second" select="$loci-array[2]"/>
  <xsl:variable name="third" select="$loci-array[3]"/>

  <xsl:variable name="locus-pair12" select="concat($first,':',$second)"/>
  <xsl:variable name="locus-pair13" select="concat($first,':',$third)"/>
  <xsl:variable name="locus-pair23" select="concat($second,':',$third)"/>

  <xsl:for-each select="haplotypefreq/haplotype[frequency &gt;=
   0.05]">

   <xsl:sort select="frequency"/>

   <xsl:call-template name="newline"/>
   <xsl:value-of select="substring(@name, 1, string-length(@name)-1)"/>
   <xsl:call-template name="newline"/>
   
   <xsl:variable name="allele-array" select="str:tokenize(substring(@name, 1,
    string-length(@name)-1), ':')"/>
   
   <xsl:variable name="allele1" select="$allele-array[1]"/>
   <xsl:variable name="allele2" select="$allele-array[2]"/>
   <xsl:variable name="allele3" select="$allele-array[3]"/>
   
   <xsl:text> Allele freq for </xsl:text>
   <xsl:value-of select="$allele1"/>
   <xsl:text> at </xsl:text>
   <xsl:value-of select="$first"/>
   <xsl:text> locus = </xsl:text>

   
   <xsl:value-of
    select="/dataanalysis/locus[@name=$first]/allelecounts/allele[@name=$allele1]/frequency"/>
   <xsl:call-template name="newline"/>
   
   <xsl:text> Allele freq for </xsl:text>
   <xsl:value-of select="$allele2"/>
   <xsl:text> at </xsl:text>
   <xsl:value-of select="$second"/>
   <xsl:text> locus = </xsl:text>
   
   <xsl:value-of select="/dataanalysis/locus[@name=$second]/allelecounts/allele[@name=$allele2]/frequency"/>
   
   <xsl:call-template name="newline"/>

   <xsl:text> Allele freq for </xsl:text>
   <xsl:value-of select="$allele3"/>
   <xsl:text> at </xsl:text>
   <xsl:value-of select="$third"/>
   <xsl:text> locus = </xsl:text>
   
   <xsl:value-of select="/dataanalysis/locus[@name=$third]/allelecounts/allele[@name=$allele3]/frequency"/>
   
   <xsl:call-template name="newline"/>

   <xsl:variable name="allele-name12"
    select="concat($allele1,':',$allele2,':')"/>
    
   <xsl:text> Haplotype freq for </xsl:text>
   <xsl:value-of select="$allele-name12"/>
   <xsl:text> at </xsl:text>
   <xsl:value-of select="$locus-pair12"/>
   <xsl:text> haplotype pair = </xsl:text>

   <xsl:value-of select="/dataanalysis/emhaplofreq/group[@loci=$locus-pair12]/haplotypefreq/haplotype[@name=$allele-name12]/frequency"/>

  </xsl:for-each>
  <xsl:call-template name="newline"/>

 </xsl:template>

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 
