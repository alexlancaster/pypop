<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <!-- ################  HOMOZYGOSITY STATISTICS ###################### --> 
 
 <xsl:template match="homozygosity">
  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">Homozygosity</xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="2"/>
   <xsl:with-param name="text">

    <xsl:choose>

     <xsl:when test="@role='out-of-range'">
      <xsl:text>*Out of range of simulated homozygosity values*</xsl:text>
      <xsl:call-template name="newline"/>
      <xsl:text>*can't estimate expected homozygosity*</xsl:text>
     </xsl:when>
     
     <xsl:otherwise>
      
      <!-- print specified fields then do templates for pvalue -->

      <xsl:text>Observed: </xsl:text>
      <xsl:value-of select="observed"/>
      <xsl:text>, Expected: </xsl:text>
      <xsl:value-of select="observed"/>
      <xsl:text>, Normalized deviate (Fnd): </xsl:text>
      <xsl:value-of select="normdev"/>
      <xsl:call-template name="newline"/>
      <xsl:text>p-value range:</xsl:text>

      <!-- treat pvalue differently, since it is not a simple value, but
      has an upper and lower bound -->
      <xsl:apply-templates select="pvalue" mode="bounded"/>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>

 <xsl:template match="pvalue" mode="bounded">
   <xsl:call-template name="append-pad">
   <xsl:with-param name="padChar">*</xsl:with-param>
   <xsl:with-param name="length">
    <xsl:call-template name="get-significance">
     <xsl:with-param name="pvalue" select="upper"/>
    </xsl:call-template>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:text> </xsl:text>
  <xsl:value-of select="lower"/><xsl:text disable-output-escaping="yes"> &lt; p &lt;= </xsl:text><xsl:value-of select="upper"/>
  
  </xsl:template>

 <!-- ################  END HOMOZYGOSITY STATISTICS ###################### --> 

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 