<!DOCTYPE xsl:stylesheet SYSTEM "xsl.dtd">
<xsl:stylesheet version='"1.0"' xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text"/>

<xsl:template match="/">
  <xsl:apply-templates/>
</xsl:template>

<xsl:template match="text()">
<!--  <xsl:value-of select="."/>  -->
</xsl:template>

<xsl:template name="newline"><xsl:text>
</xsl:text></xsl:template>

  <xsl:template match="dataanalysis">
  <xsl:text>Results of data analysis</xsl:text>
  <xsl:call-template name="newline"/>
  <xsl:text>Performed on the '</xsl:text><xsl:value-of select="filename"/><xsl:text>' file at: </xsl:text><xsl:value-of select="@date"/>
  <xsl:call-template name="newline"/>
  <xsl:call-template name="newline"/>
  <xsl:apply-templates/>
  </xsl:template>

  <!-- Leave blank -->
  <xsl:template match="filename"></xsl:template>

  <xsl:template match="populationdata">
  <xsl:text>Population Summary</xsl:text>
  <xsl:call-template name="newline"/>
  <xsl:text>==================</xsl:text>
  <xsl:call-template name="newline"/>
  <xsl:call-template name="newline"/>
  <xsl:apply-templates/>
</xsl:template>

  <xsl:template match="longitude|latitude|ethnicgroup|collectionsite|typingmethod|continentoforigin|labcode">
    <xsl:text>*</xsl:text>
    <xsl:value-of select="name(.)"/>
    <xsl:text>*: </xsl:text>
    <xsl:value-of select="."/>
    <xsl:call-template name="newline"/>
  </xsl:template>

  <xsl:template match="populationdata/totals">
   <xsl:call-template name="newline"/>
   <xsl:text>Population Totals</xsl:text>
   <xsl:call-template name="newline"/>
   <xsl:text>=================</xsl:text>
   <xsl:call-template name="newline"/>
   <xsl:call-template name="newline"/>
   <xsl:apply-templates/>
  </xsl:template>

  <xsl:template match="indivcount">
   <xsl:text>Sample Size (n): </xsl:text>
   <xsl:value-of select="."/>
   <xsl:call-template name="newline"/>
  </xsl:template>

  <xsl:template match="allelecount">
   <xsl:text>Allele Count (2n): </xsl:text>
   <xsl:value-of select="."/>
   <xsl:call-template name="newline"/>
  </xsl:template>

  <xsl:template match="locuscount">
   <xsl:text>Total Loci: </xsl:text>
   <xsl:value-of select="."/>
   <xsl:call-template name="newline"/>
  </xsl:template>


</xsl:stylesheet>
