<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exslt="http://exslt.org/common"
 extension-element-prefixes="exslt"
 xmlns:data="any-uri">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>

 <data:phylip-loci>
  <loci><locus>A</locus><locus>B</locus></loci>
  <loci><locus>B</locus><locus>C</locus></loci>
  <loci><locus>DRB1</locus><locus>DQB1</locus></loci>
  <loci><locus>A</locus><locus>B</locus><locus>DRB</locus></loci>
  <loci><locus>DRB1</locus><locus>DPB1</locus></loci>
 </data:phylip-loci>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>
  
 <xsl:variable name="all-haplo-list" select="document('haplolist-by-group.xml', .)/haplolist-by-group"/>

 <xsl:template name="phylip-haplos">
  <xsl:param name="node" select="."/>
  <xsl:param name="loci-to-output"/>

  <xsl:text>     </xsl:text>
  <xsl:value-of select="count($node)"/>
  <xsl:text> </xsl:text>
  <xsl:text>1</xsl:text>
  <xsl:call-template name="newline"/>

  <xsl:variable name="haplolist-curlocus"
    select="$all-haplo-list/group[@loci=$loci-to-output]"/>
  <xsl:value-of select="count($haplolist-curlocus/haplotype)"/>   
  <xsl:text> </xsl:text>

  <xsl:call-template name="newline"/>

  <xsl:for-each select="$node">

   <xsl:sort select="populationdata/popname"/>

   <xsl:call-template name="append-pad">
    <xsl:with-param name="padVar">
     <xsl:value-of select="populationdata/popname"/>
    </xsl:with-param>
    <xsl:with-param name="length" select="9"/>
   </xsl:call-template>
   <xsl:text> </xsl:text>

   <xsl:variable name="cur-haplo-list" select="emhaplofreq/group[@loci=$loci-to-output]/haplotypefreq/haplotype"/>

   <xsl:for-each select="$haplolist-curlocus/haplotype">
    <xsl:variable name="haplotype" select="."/>
    <xsl:choose>
     <xsl:when test="$cur-haplo-list[@name=$haplotype]">
      <xsl:value-of select="normalize-space($cur-haplo-list[@name=$haplotype]/frequency)"/>
     </xsl:when>
     <xsl:otherwise>0.00000</xsl:otherwise>
    </xsl:choose>
    <xsl:text> </xsl:text>
    </xsl:for-each>

   <xsl:call-template name="newline"/>
   
  </xsl:for-each>

 </xsl:template>
 
 <xsl:template match="/">

  <exslt:document href="A-B.haplo.phy"
   omit-xml-declaration="yes"
   method="text">
   <xsl:call-template name="phylip-haplos">
    <xsl:with-param name="node" select="/meta/dataanalysis[emhaplofreq/group/@loci='A:B']"/>
    <xsl:with-param name="loci-to-output" select="'A:B'"/>
   </xsl:call-template>
  </exslt:document>

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
