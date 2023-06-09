<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exslt="http://exslt.org/common"
 exclude-result-prefixes="exslt">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="xml"  encoding="utf8" omit-xml-declaration="yes"/>

 <!-- unique key for all loci -->
 <xsl:key name="alleles" match="allele" use="."/>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>
 

 <xsl:template match="/output">
  <allelelist-by-locus>
   <xsl:call-template name="newline"/>
   <xsl:for-each select="locus">
   <locus>
    <xsl:attribute name="name">
     <xsl:value-of select="@name"/>
    </xsl:attribute>

    <!--
    <xsl:message>
    <xsl:value-of select="count(population/allelecounts/allele)"/>
    <xsl:text>: </xsl:text>
    <xsl:variable name="sort-by" select="'@name'"/>
    <xsl:for-each select="population/allelecounts/allele">
    <xsl:value-of select="@name"/>
      <xsl:text> </xsl:text>
   </xsl:for-each>
    </xsl:message>
    -->

    <xsl:variable name="all-alleles">
     <xsl:for-each select="population/allelecounts/allele">
      <allele>
       <xsl:value-of select="@name"/>
      </allele>
    </xsl:for-each>

    </xsl:variable>

    <xsl:variable name="all-distinct-alleles"
     select="exslt:node-set($all-alleles)/allele[not(.=following::allele)]"/>

    <xsl:for-each select="$all-distinct-alleles">
     <allele>
     <xsl:value-of select="."/>
    </allele>
    </xsl:for-each>

   </locus>   
   <xsl:call-template name="newline"/>
   </xsl:for-each>
  </allelelist-by-locus>
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
