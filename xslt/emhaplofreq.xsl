<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:data="any-uri">

 <!-- #################  HAPLOTYPE/LD STATISTICS ###################### --> 

 <xsl:template match="emhaplofreq">
  <xsl:call-template name="header">
   <xsl:with-param name="title">Haplotype/LD stats via emhaplofreq: <xsl:value-of select="../@loci"/>
   </xsl:with-param>
  </xsl:call-template>
  <xsl:call-template name="newline"/>
  <xsl:apply-templates/> 
  <xsl:call-template name="newline"/>

  <xsl:call-template name="pairwise-ld">
   <xsl:with-param name="loci" 
    select="group[@mode='all-pairwise-ld-with-permu' or 
    @mode='all-pairwise-ld-no-permu']"/>
  </xsl:call-template>

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
  <xsl:call-template name="newline"/>

  <xsl:apply-templates select="haplotypefreq"/>

  <xsl:call-template name="newline"/>

  <xsl:apply-templates select="linkagediseq"/>

 </xsl:template>


 <xsl:template match="emhaplofreq/group[@mode='LD']">

   <xsl:call-template name="header">
    <xsl:with-param name="title">LD est. for loci: <xsl:value-of select="@loci"/>
    </xsl:with-param>
   </xsl:call-template>
   <xsl:call-template name="newline"/>

  <xsl:call-template name="linesep-fields">
   <xsl:with-param name="nodes" select="uniquepheno|uniquegeno|haplocount|loglikelihood|individcount"/>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

  <xsl:apply-templates select="linkagediseq"/>

  <xsl:call-template name="newline"/>

  <xsl:apply-templates select="permutationSummary"/>

  <xsl:call-template name="newline"/>
 </xsl:template>

 <xsl:template match="emhaplofreq/group"/>

 <xsl:template name="pairwise-ld">
  <xsl:param name="loci"/>
  
  <xsl:call-template name="header">
   <xsl:with-param name="title">all pairwise LD est. for loci
   </xsl:with-param>
  </xsl:call-template>

  <xsl:call-template name="newline"/>

  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar">Locus pair</xsl:with-param>
   <xsl:with-param name="length" select="10"/>
   <xsl:with-param name="type" select="'left'"/>
  </xsl:call-template>
   
  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar">D'</xsl:with-param>
   <xsl:with-param name="length" select="10"/>
   <xsl:with-param name="type" select="'right'"/>
  </xsl:call-template>
  
  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar">Wn</xsl:with-param>
   <xsl:with-param name="length" select="10"/>
   <xsl:with-param name="type" select="'right'"/>
  </xsl:call-template>
  
  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar"># permu</xsl:with-param>
   <xsl:with-param name="length" select="10"/>
   <xsl:with-param name="type" select="'right'"/>
  </xsl:call-template>
  
  <xsl:call-template name="justified-cell">
   <xsl:with-param name="padVar"> p-value</xsl:with-param>
   <xsl:with-param name="length" select="10"/>
   <xsl:with-param name="type" select="'left'"/>
  </xsl:call-template>

  <xsl:call-template name="newline"/>

  <xsl:for-each select="$loci">

   <xsl:if test="@role!='no-data'">

    <xsl:variable name="locus-pair" select="@loci"/>

    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar" select="$locus-pair"/>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'left'"/>
    </xsl:call-template>
   
    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar" select="linkagediseq/summary/dprime"/>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>
    
    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar" select="linkagediseq/summary/wn"/>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>

    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar" select="permutationSummary/pvalue/@totalperm"/>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'right'"/>
    </xsl:call-template>

    <xsl:call-template name="justified-cell">
     <xsl:with-param name="padVar">
      <xsl:text> </xsl:text>
      <xsl:apply-templates select="permutationSummary/pvalue"/>
     </xsl:with-param>
     <xsl:with-param name="length" select="10"/>
     <xsl:with-param name="type" select="'left'"/>
    </xsl:call-template>


    <xsl:call-template name="newline"/>
   </xsl:if>
   
<!--
    <xsl:call-template name="linesep-fields">
     <xsl:with-param name="nodes" select="dprime|wn|q/chisq|q/dof"/>
    </xsl:call-template>
    -->
   
  </xsl:for-each>

 </xsl:template>


<!--
  <xsl:call-template name="linesep-fields">
   <xsl:with-param name="nodes" select="uniquepheno|uniquegeno|haplocount|loglikelihood|individcount"/>
  </xsl:call-template>
  <xsl:call-template name="newline"/>

-->

<!--

  <xsl:call-template name="newline"/>

  <xsl:apply-templates select="haplotypefreq"/>

  <xsl:call-template name="newline"/>

  <xsl:apply-templates select="linkagediseq"/>

  <xsl:call-template name="newline"/>

  <xsl:apply-templates select="permutationSummary"/>

  <xsl:call-template name="newline"/>
-->


 <xsl:template match="haplotypefreq">

  <xsl:choose>
   <xsl:when test="condition/@role='converged'">

    <!-- create header for table -->
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar">haplotype</xsl:with-param>
     <xsl:with-param name="length">24</xsl:with-param>
    </xsl:call-template>
    
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar">frequency</xsl:with-param>
     <xsl:with-param name="length">24</xsl:with-param>
    </xsl:call-template>
    
    <xsl:call-template name="append-pad">
     <xsl:with-param name="padVar">num. of copies</xsl:with-param>
     <xsl:with-param name="length">24</xsl:with-param>
    </xsl:call-template>
    
    <xsl:call-template name="newline"/>
    
    <!-- loop through each haplotype-->
    <xsl:for-each select="haplotype">
     <xsl:sort select="@name" data-type="text" order="ascending"/>
     <xsl:for-each select="frequency|numCopies|@name">
      <xsl:call-template name="append-pad">
       <xsl:with-param name="padVar" select="."/>
       <xsl:with-param name="length">24</xsl:with-param>
      </xsl:call-template>
     </xsl:for-each>
     <xsl:call-template name="newline"/>
    </xsl:for-each>

   </xsl:when>

   <xsl:when test="condition/@role='loglike-failed-converge'">
    <xsl:text>Log likelihood failed to converge in specified number of iterations.
    </xsl:text>
   </xsl:when>

   <xsl:otherwise>
    <xsl:text>Unhandled 'role': </xsl:text> <xsl:value-of
    select="condition/@role"/> 

    <xsl:text>' Please implement.</xsl:text>
   </xsl:otherwise>

  </xsl:choose>

 </xsl:template>

 <xsl:template match="linkagediseq">

  <xsl:choose>
   <xsl:when test="../haplotypefreq/condition/@role='converged'">
    
    <xsl:for-each select="summary">
     <xsl:text>LD summary statistics between: </xsl:text>
     <xsl:variable name="loci" select="../../@loci"/>
     
     <xsl:call-template name="get-nth-element">
      <xsl:with-param name="delim">:</xsl:with-param>
      <xsl:with-param name="str" select="$loci"/>
      <xsl:with-param name="n" select="@first"/>
     </xsl:call-template>
     
     <xsl:text> and </xsl:text>
     
     <xsl:call-template name="get-nth-element">
      <xsl:with-param name="delim">:</xsl:with-param>
      <xsl:with-param name="str" select="$loci"/>
      <xsl:with-param name="n" select="@second"/>
     </xsl:call-template>
     
     <xsl:call-template name="newline"/>
     
     <xsl:call-template name="linesep-fields">
      <xsl:with-param name="nodes" select="dprime|wn|q/chisq|q/dof"/>
     </xsl:call-template>
     
    </xsl:for-each>
   
   </xsl:when>  

   <xsl:when test="../haplotypefreq/condition/@role='loglike-failed-converge'">
    <xsl:text>Log likelihood failed to converge: don't calculate any LD stats.</xsl:text>

    <xsl:call-template name="newline"/>
   </xsl:when>

   <xsl:otherwise>
    <xsl:text>Unhandled 'role': Please implement!</xsl:text>

    <xsl:call-template name="newline"/>
   </xsl:otherwise>

  </xsl:choose>

  <xsl:call-template name="newline"/>

 </xsl:template>

 <xsl:template match="permutationSummary">
  <xsl:text>LD significance test:</xsl:text>

  <xsl:call-template name="newline"/>

  <xsl:apply-templates select="pvalue"/>
  <xsl:text> from </xsl:text>
  <xsl:value-of select="pvalue/@totalperm"/>
  <xsl:text> permutations</xsl:text>
  <xsl:call-template name="newline"/>

 </xsl:template>

 <!-- ################# END  HAPLOTYPE/LD STATISTICS ################### --> 

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 