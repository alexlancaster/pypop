<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exslt="http://exslt.org/common"
 exclude-result-prefixes="exslt">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="xml" encoding="utf8" omit-xml-declaration="yes"/>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>

 <xsl:template match="/meta/dataanalysis[1]">

  <haplolist-by-group>
   <xsl:call-template name="newline"/>

   <xsl:for-each select="emhaplofreq/group">
    <xsl:variable name="curloci" select="@loci"/>

    <group>
     <xsl:attribute name="loci">
       <xsl:value-of select="$curloci"/>
     </xsl:attribute>

    <xsl:variable name="all-haplotypes">
     <xsl:for-each select="/meta/dataanalysis/emhaplofreq/group[@loci=$curloci]/haplotypefreq/haplotype">
      <haplotype>
       <xsl:value-of select="@name"/>
      </haplotype>
    </xsl:for-each>

    </xsl:variable>

    <xsl:variable name="all-distinct-haplotypes"
     select="exslt:node-set($all-haplotypes)/haplotype[not(.=following::haplotype)]"/>

    <xsl:for-each select="$all-distinct-haplotypes">
     <haplotype>
       <xsl:value-of select="."/>
      </haplotype>
    </xsl:for-each>

   </group>
   <xsl:call-template name="newline"/>
   </xsl:for-each>
  </haplolist-by-group>

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
