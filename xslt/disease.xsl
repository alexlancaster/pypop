<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <xsl:import href="common.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes"/>

 <xsl:template match="hardyweinbergGuoThompson"/>	

 <xsl:template match="emhaplofreq"/>	

 <xsl:template match="allelecounts">
  <xsl:call-template name="locus-header">
   <xsl:with-param name="title">Allele Counts</xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <xsl:choose>
  
   <!-- if there's no data, don't do anything -->
   <xsl:when test="@role='no-data'">
    <xsl:text>No allele data!</xsl:text>
    <xsl:call-template name="newline"/>
   </xsl:when>
   
   <xsl:otherwise>
    <!-- do all the non-allelecount templates -->
    <xsl:apply-templates select="*[not(self::allele)]"/>

    <xsl:call-template name="newline"/>

    <!-- create a header for table -->
    <xsl:text>Name      Frequency (Count)</xsl:text>
    <xsl:call-template name="newline"/>
    
    <!-- loop through each allele-->
    <xsl:for-each select="allele">
     <xsl:sort select="count" data-type="number" order="descending"/>
     <xsl:for-each select="frequency|count|@name">
      <xsl:call-template name="append-pad">
       <xsl:with-param name="padVar" select="."/>
       <xsl:with-param name="length">10</xsl:with-param>
      </xsl:call-template>
     </xsl:for-each>
     <xsl:call-template name="newline"/>
    </xsl:for-each>
    
    <!-- print out the totals at end of table -->
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar">Total</xsl:with-param>
     <xsl:with-param name="length" select="10"/>
    </xsl:call-template>
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar" select="totalfrequency"/>
     <xsl:with-param name="length" select="10"/>
    </xsl:call-template>
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar" select="totalcount"/>
     <xsl:with-param name="length" select="10"/>
    </xsl:call-template>
    <xsl:call-template name="newline"/>

    <xsl:call-template name="newline"/>
    <xsl:text>Sorted by allele name:</xsl:text>
    <xsl:call-template name="newline"/>
    <!-- loop through each allele-->
    <xsl:for-each select="allele">
     <xsl:sort select="@name" data-type="number" order="ascending"/>
     <xsl:for-each select="frequency|count|@name">
      <xsl:call-template name="append-pad">
       <xsl:with-param name="padVar" select="."/>
       <xsl:with-param name="length">10</xsl:with-param>
      </xsl:call-template>
     </xsl:for-each>
     <xsl:call-template name="newline"/>
    </xsl:for-each>
   </xsl:otherwise>
  </xsl:choose>

  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Haplotype/LD stats via emhaplofreq: <xsl:value-of select="../@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
  <xsl:apply-templates/>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='no-data']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">No data left after filtering at: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='too-many-lines']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Too many rows for haplotype programme: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group[@mode='haplo']">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Haplotype frequency est. for loci: <xsl:value-of select="@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <xsl:call-template name="linesep-fields">
   <xsl:with-param name="nodes" select="uniquepheno|uniquegeno|haplocount|loglikelihood|individcount"/>
  </xsl:call-template>

  <!-- mpn having a go -->
  <xsl:call-template name="newline"/>
  <!-- loop through each haplotype-->
  <xsl:for-each select="haplotypefreq/haplotype">
   <xsl:sort select="@name" data-type="number" order="ascending"/>
   <xsl:for-each select="frequency|numCopies|@name">
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar" select="."/>
     <xsl:with-param name="length">24</xsl:with-param>
    </xsl:call-template>
   </xsl:for-each>
   <xsl:call-template name="newline"/>
  </xsl:for-each>

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
