<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>
 
 <xsl:template match="/">
  <xsl:apply-templates/>
 </xsl:template>

 <xsl:template name="genlist">
  <xsl:param name="nodes" select="."/>
  <xsl:param name="delim"></xsl:param>
  
 </xsl:template>

 <xsl:template match="allelecounts[@role!='no-data']">

  <!-- initialize a vector with appropriate number of bins -->
  <xsl:text>allele.counts = rep(c(0),</xsl:text><xsl:value-of
   select="count(allele)"/><xsl:text>)
</xsl:text>
  <xsl:text>allele.freq = rep(c(0),</xsl:text><xsl:value-of
   select="count(allele)"/><xsl:text>)
</xsl:text>
  <xsl:text>allele.names = rep(c("*"),</xsl:text><xsl:value-of
   select="count(allele)"/><xsl:text>)
</xsl:text>

  <!-- loop through alleles and assign each vector with count and label -->
  <xsl:for-each select="allele">
   <xsl:sort select="count" data-type="number" order="descending"/>
   <xsl:text>allele.counts[</xsl:text><xsl:value-of select="position()"/>
   <xsl:text>] = </xsl:text>
   <xsl:value-of select="count"/>
   <xsl:text>
</xsl:text>
<xsl:text>allele.freq[</xsl:text><xsl:value-of select="position()"/>
   <xsl:text>] = </xsl:text>
   <xsl:value-of select="frequency"/>
   <xsl:text>
</xsl:text>
   <xsl:text>allele.names[</xsl:text><xsl:value-of select="position()"/>
   <xsl:text>] = "</xsl:text>
   <xsl:value-of select="@name"/>
   <xsl:text>"
</xsl:text>
  </xsl:for-each>
<xsl:text>allele.counts
names(allele.counts) = allele.names
names(allele.freq) = allele.names
postscript("</xsl:text><xsl:value-of select="substring-after(../@name,'*')"/><xsl:text>.ps")
barplot(allele.freq,las=2)
title("Allele frequencies for locus </xsl:text><xsl:value-of select="../@name"/><xsl:text>")
rm(allele.counts)
rm(allele.names)

</xsl:text>
  
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
